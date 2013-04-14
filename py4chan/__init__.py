"""
    py-4chan
    ~~~~~~~~

    Python Wrappers to access 4chan's API.

    This program is free software. It comes without any warranty, to
    the extent permitted by applicable law. You can redistribute it
    and/or modify it under the terms of the Do What The Fuck You Want
    To Public License, Version 2, as published by Sam Hocevar. See
    http://sam.zoy.org/wtfpl/COPYING for more details.

"""

# Using requests-transition to use older version of requests, 0.14, in the meantime
import requests0 as requests
from datetime import datetime
import base64

_4CHAN_API = 'api.4chan.org'
_4CHAN_BOARDS_URL = 'boards.4chan.org'
_4CHAN_IMAGES_URL = 'images.4chan.org'
_4CHAN_THUMBS_URL = '0.thumbs.4chan.org'
_BOARD = '%s/%i.json'
_THREAD = '%s/res/%i.json'
_VERSION = '0.1.3'

class Board(object):
    def __init__(self, boardName, https = False, apiUrl = _4CHAN_API, session = None):
        self._https = https
        self._base_url = ('http://' if not https else 'https://') + apiUrl
        self._board_name = boardName
        self._requests_session = session or requests.session(headers = {'User-Agent': 'py-4chan/%s' % _VERSION})
        self._thread_cache = {}

    def getThread(self, id, updateIfCached = True):
        """
            Get a thread from 4chan via 4chan API.

            :param id: thread ID
            :param updateIfCached: Should the thread be updated if it's found in the cache?
            :return: Thread
        """
        if id in self._thread_cache:
            thread = self._thread_cache[id]
            if updateIfCached:
                thread.update()

            return thread

        url = '%s/%s' % (self._base_url, _THREAD % (self._board_name, id))
        res = self._requests_session.get(url)

        thread = Thread._fromRequest(self, res, id)
        self._thread_cache[id] = thread

        return thread

    def threadExists(self, id):
        """
            Check if a thread exists, or is 404.
            :param id: thread ID
            :return: bool
        """
        url = '%s/%s' % (self._base_url, _THREAD % (self._board_name, id))
        return self._requests_session.head(url).status_code == 200

    def getThreads(self, page = 1):
        """
            Get thread on pages, if the thread is already in cache, return cached thread entry.

            Sets thread.want_update to True if the thread is being returned from the cache.
            :param: page: page to fetch thread from
            :return: list[Thread]
        """
        page -= 1
        url = '%s/%s' % (self._base_url, _BOARD % (self._board_name,page))
        res = self._requests_session.get(url)
        if res.status_code != 200:
            res.raise_for_status()

        json = res.json
        threads = []
        for thread_json in json['threads']:
            id = thread_json['posts'][0]['no']
            if id in self._thread_cache:
                thread = self._thread_cache[id]
                thread.want_update = True
            else:
                thread = Thread._fromJson(thread_json, self)
                self._thread_cache[thread.id] = thread

            threads.append(thread)

        return threads



    @property
    def Name(self):
        """
            Board name that this board represents.
            :return: string
        """
        return self._board_name


class Thread(object):
    def __init__(self, board, id):
        self._board = board
        self.id = id
        self.topic = None
        self.replies = []
        self.is_404 = False
        self.last_reply_id = 0
        self.omitted_posts = 0
        self.omitted_images = 0
        self.want_update = False
        self._last_modified = None

    @property
    def Closed(self):
        """
            Is the thread closed?
            :return: bool
        """
        return self.topic._data['closed'] == 1

    @property
    def Sticky(self):
        """
            Is the thread sticky?
            :return: bool
        """
        return self.topic._data['sticky'] == 1

    @staticmethod
    def _fromRequest(board, res, id):
        if res.status_code == 404:
            return None

        elif res.status_code == 200:
            return Thread._fromJson(res.json, board, id, res.headers['last-modified'])

        else:
            res.raise_for_status()

    @staticmethod
    def _fromJson(json, board, id = None, last_modified = None):
        t = Thread(board, id)
        t._last_modified = last_modified

        posts = json['posts']


        t.topic = Post(t, posts[0])
        t.replies.extend(Post(t, p) for p in posts[1:])

        if id is not None:
            if not t.replies:
                t.last_reply_id = t.topic.PostNumber
            else:
                t.last_reply_id = t.replies[-1].PostNumber

        else:
            t.want_update = True
            head = posts[0]
            t.id = head['no']
            try:
                t.omitted_images = head['omitted_images']
                t.omitted_posts = head['omitted_posts']

            except KeyError:
                pass

        return t


    def Files(self):
        """
            Returns a generator that yields all the URL of all the files (not thumbnails) in the thread.
        """
        yield self.topic.FileUrl
        for reply in self.replies:
            if reply.HasFile:
                yield reply.FileUrl

    def Thumbs(self):
        """
            Returns a generator that yields all the URL of all the thumbnails in the thread.
        """
        yield self.topic.ThumbnailUrl
        for reply in self.replies:
            if reply.HasFile:
                yield reply.ThumbnailUrl

    def update(self, force = False):
        """
            Fetch new posts from the server. Returns an integer with the number of new posts.
            :param: force: Force thread update.
            :return: int: How many new posts fetched.
        """

        # The thread has already 404'ed, this function shouldn't do anything anymore.
        if self.is_404 and not force:
            return 0

        url = '%s/%s' % (self._board._base_url, _THREAD % (self._board._board_name, self.id))
        if self._last_modified:
            headers = {'If-Modified-Since': self._last_modified}
        else:
            headers = None

        res = self._board._requests_session.get(url, headers = headers)

        # 304 Not Modified, no new posts.
        if res.status_code == 304:
            return 0

        # 404 Not Found, thread died.
        elif res.status_code == 404:
            self.is_404 = True
            # remove post from cache, because it's gone.
            self._board._thread_cache.pop(self.id, None)
            return 0


        elif res.status_code == 200:
            # If we somehow 404'ed, we should put ourself back in the cache.
            if self.is_404:
                self.is_404 = False
                self._board._thread_cache[self.id] = self

            # Remove
            self.want_update = False
            self.omitted_images = 0
            self.omitted_posts = 0

            self._last_modified = res.headers['last-modified']
            posts = res.json['posts']

            originalPostCount = len(self.replies)
            self.topic = Post(self, posts[0])
            if self.last_reply_id and not force:
                self.replies.extend(Post(self, p) for p in posts if p['no'] > self.last_reply_id)
            else:
                self.replies[:] = [Post(self, p) for p in posts[1:]]
            newPostCount = len(self.replies)
            postCountDelta = newPostCount - originalPostCount
            if not postCountDelta:
                return 0

            self.last_reply_id = self.replies[-1].PostNumber

            return postCountDelta

        else:
            res.raise_for_status()

    def __repr__(self):
        extra = ""
        if self.omitted_images or self.omitted_posts:
            extra = ", %i omitted images, %i omitted posts" % (
                self.omitted_images, self.omitted_posts
            )

        return '<Thread /%s/%i, %i replies%s>' % (
            self._board.Name, self.id, len(self.replies), extra
        )


class Post(object):
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data

    @property
    def PostNumber(self):
        """
            :return: int
        """
        return self._data['no']

    @property
    def Id(self):
        """
            :return: int
        """
        return self._data.get('id')

    @property
    def Name(self):
        return self._data.get('name', None)

    @property
    def EMail(self):
        return self._data.get('email', None)

    @property
    def Tripcode(self):
        return self._data.get('tripcode', None)

    @property
    def Subject(self):
        return self._data.get('sub', None)
    
    @property
    def Comment(self):
        return self._data.get('com', None)

    @property
    def Timestamp(self):
        return self._data['time']

    @property
    def Datetime(self):
        return datetime.fromtimestamp(self._data['time'])

    @property
    def FileMd5(self):
        if not self.HasFile:
            return None

        return base64.b64decode(self._data['md5'])

    @property
    def FileMd5Hex(self):
        if not self.HasFile:
            return None

        return self.FileMd5.encode('hex')

    @property
    def FileUrl(self):
        if not self.HasFile:
            return None

        board = self._thread._board
        
        return '%s://%s/%s/src/%i%s' % (
            'https' if board._https else 'http',
            _4CHAN_IMAGES_URL,
            board.Name,
            self._data['tim'],
            self._data['ext']
        )
    
    @property
    def FileExtension(self):
        return self._data.get('ext', None)

    @property
    def FileSize(self):
        return self._data.get('fsize', None)
    
    @property
    def FileWidth(self):
        return self._data.get('w', None)
    
    @property
    def FileHeight(self):
        return self._data.get('h', None)

    @property
    def FileDeleted(self):
        return self._data.get('filedeleted', 0) == 1

    @property
    def ThumbnailWidth(self):
        return self._data.get('tn_w', None)

    @property
    def ThumbnailHeight(self):
        return self._data.get('tn_h', None)

    @property
    def ThumbnailUrl(self):
        if not self.HasFile:
            return None

        board = self._thread._board

        return '%s://%s/%s/thumb/%is.jpg' % (
            'https' if board._https else 'http',
            _4CHAN_THUMBS_URL,
            board.Name,
            self._data['tim']
        )

    @property
    def HasFile(self):
        return 'filename' in self._data

    def FileRequest(self):
        return self._thread._board._requests_session.get(self.FileUrl)

    def ThumbnailRequest(self):
        return self._thread._board._requests_session.get(self.ThumbnailUrl)

    @property
    def PostUrl(self):
        board = self._thread._board
        return "%s://%s/%s/res/%i#p%i" % (
            'https' if board._https else 'http',
            _4CHAN_BOARDS_URL,
            board.Name,
            self._thread.id,
            self.PostNumber
        )

    def __repr__(self):
        return "<Post /%s/%i#%i, hasFile: %r>" % (
            self._thread._board.Name,
            self._thread.id,
            self.PostNumber,
            self.HasFile
        )
