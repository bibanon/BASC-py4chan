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

import requests
from datetime import datetime

_4CHAN_BOARDS_URL = 'boards.4chan.org'
_4CHAN_API = 'a.4cdn.org'
_4CHAN_IMAGES_URL = 'i.4cdn.org'
_4CHAN_THUMBS_URL = '0.t.4cdn.org'

#_4CHAN_BOARDS_URL = 'boards.4chan.org'
#_4CHAN_API = 'api.4chan.org'
#_4CHAN_IMAGES_URL = 'images.4chan.org'
#_4CHAN_THUMBS_URL = '0.thumbs.4chan.org'

_BOARD = '%s/%i.json'
_THREAD = '%s/res/%i.json'
_VERSION = '0.3'

class Board(object):
    def __init__(self, board_name, https = False, api_url = _4CHAN_API, session = None):
        self._https = https
        self._base_url = ('http://' if not https else 'https://') + api_url
        self._board_name = board_name
        
        # requests 1.x updated calls
        self._requests_session = session or requests.session()
        self._requests_session.headers = {'User-Agent': 'py-4chan/%s' % _VERSION}
        # requests 0.14 vintage code
#        self._requests_session = session or requests.session(headers = {'User-Agent': 'py-4chan/%s' % _VERSION})
        
        self._thread_cache = {}

    def get_thread(self, id, update_if_cached = True):
        """
            Get a thread from 4chan via 4chan API.

            :param id: thread ID
            :param updateIfCached: Should the thread be updated if it's found in the cache?
            :return: Thread
        """
        if id in self._thread_cache:
            thread = self._thread_cache[id]
            if update_if_cached:
                thread.update()

            return thread

        url = '%s/%s' % (self._base_url, _THREAD % (self._board_name, id))
        res = self._requests_session.get(url)

        thread = Thread._from_request(self, res, id)
        self._thread_cache[id] = thread

        return thread

    def thread_exists(self, id):
        """
            Check if a thread exists, or is 404.
            :param id: thread ID
            :return: bool
        """
        url = '%s/%s' % (self._base_url, _THREAD % (self._board_name, id))
        return self._requests_session.head(url).status_code == 200

    def get_threads(self, page = 1):
        """
            Get thread on pages, if the thread is already in cache, return cached thread entry.

            Sets thread.want_update to True if the thread is being returned from the cache.
            :param: page: page to fetch thread from
            :return: list[Thread]
        """
        page -= 1
        url = '%s/%s' % (self._base_url, _BOARD % (self._board_name, page))
        res = self._requests_session.get(url)
        if res.status_code != 200:
            res.raise_for_status()

        json = res.json()
        threads = []
        for thread_json in json['threads']:
            id = thread_json['posts'][0]['no']
            if id in self._thread_cache:
                thread = self._thread_cache[id]
                thread.want_update = True
            else:
                thread = Thread._from_json(thread_json, self)
                self._thread_cache[thread.id] = thread

            threads.append(thread)

        return threads



    @property
    def name(self):
        """
            Board name that this board represents.
            :return: string
        """
        return self._board_name

    def __repr__(self):
        return '<Board /%s/>' % self.name

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
    def closed(self):
        """
            Is the thread closed?
            :return: bool
        """
        return self.topic._data.get('closed', 0) == 1

    @property
    def sticky(self):
        """
            Is the thread sticky?
            :return: bool
        """
        return self.topic._data.get('sticky', 0) == 1

    @staticmethod
    def _from_request(board, res, id):
        if res.status_code == 404:
            return None

        elif res.status_code == 200:
            return Thread._from_json(res.json(), board, id, res.headers['last-modified'])

        else:
            res.raise_for_status()

    @staticmethod
    def _from_json(json, board, id = None, last_modified = None):
        t = Thread(board, id)
        t._last_modified = last_modified

        posts = json['posts']


        t.topic = Post(t, posts[0])
        t.replies.extend(Post(t, p) for p in posts[1:])

        if id is not None:
            if not t.replies:
                t.last_reply_id = t.topic.post_number
            else:
                t.last_reply_id = t.replies[-1].post_number

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


    def files(self):
        """
            Returns a generator that yields all the URLs of all the files (not thumbnails) in the thread.
        """
        yield self.topic.file_url
        for reply in self.replies:
            if reply.has_file:
                yield reply.file_url

    def thumbs(self):
        """
            Returns a generator that yields all the URLs of all the thumbnails in the thread.
        """
        yield self.topic.thumbnail_url
        for reply in self.replies:
            if reply.has_file:
                yield reply.thumbnail_url

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
            posts = res.json()['posts']

            original_post_count = len(self.replies)
            self.topic = Post(self, posts[0])
            if self.last_reply_id and not force:
                self.replies.extend(Post(self, p) for p in posts if p['no'] > self.last_reply_id)
            else:
                self.replies[:] = [Post(self, p) for p in posts[1:]]
            new_post_count = len(self.replies)
            post_count_delta = new_post_count - original_post_count
            if not post_count_delta:
                return 0

            self.last_reply_id = self.replies[-1].post_number

            return post_count_delta

        else:
            res.raise_for_status()

    @property
    def all_posts(self):
        return [self.topic] + self.replies

    @property
    def thread_url(self):
        board = self._board
        return "%s://%s/%s/res/%i" % (
            'https' if board._https else 'http',
            _4CHAN_BOARDS_URL,
            board.name,
            self.id
        )

    def __repr__(self):
        extra = ""
        if self.omitted_images or self.omitted_posts:
            extra = ", %i omitted images, %i omitted posts" % (
                self.omitted_images, self.omitted_posts
            )

        return '<Thread /%s/%i, %i replies%s>' % (
            self._board.name, self.id, len(self.replies), extra
        )


class Post(object):
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data

    @property
    def post_number(self):
        """
            :return: int
        """
        return self._data['no']

    @property
    def id(self):
        """
            :return: int
        """
        return self._data.get('id')     # dict.get() returns None if not found

    @property
    def name(self):
        return self._data.get('name')

    @property
    def email(self):
        return self._data.get('email')

    @property
    def tripcode(self):
        return self._data.get('tripcode')

    @property
    def subject(self):
        return self._data.get('sub')
    
    @property
    def comment(self):
        return self._data.get('com')

    @property
    def timestamp(self):
        return self._data['time']

    @property
    def datetime(self):
        return datetime.fromtimestamp(self._data['time'])

    @property
    def file_md5(self):
        if not self.HasFile:
            return None

        return self._data['md5'].decode('base64')

    @property
    def file_md5_hex(self):
        if not self.has_file:
            return None

        return self.file_md5.encode('hex')

    @property
    def file_url(self):
        if not self.has_file:
            return None

        board = self._thread._board
        
        return '%s://%s/%s/src/%i%s' % (
            'https' if board._https else 'http',
            _4CHAN_IMAGES_URL,
            board.name,
            self._data['tim'],
            self._data['ext']
        )
    
    @property
    def file_extension(self):
        return self._data.get('ext')

    @property
    def file_size(self):
        return self._data.get('fsize')
    
    @property
    def file_width(self):
        return self._data.get('w')
    
    @property
    def file_height(self):
        return self._data.get('h')

    @property
    def file_deleted(self):
        return self._data.get('filedeleted', 0) == 1

    @property
    def thumbnail_width(self):
        return self._data.get('tn_w')

    @property
    def thumbnail_height(self):
        return self._data.get('tn_h')

    @property
    def thumbnail_url(self):
        if not self.HasFile:
            return None

        board = self._thread._board

        return '%s://%s/%s/thumb/%is.jpg' % (
            'https' if board._https else 'http',
            _4CHAN_THUMBS_URL,
            board.name,
            self._data['tim']
        )

    @property
    def has_file(self):
        return 'filename' in self._data

    def file_request(self):
        return self._thread._board._requests_session.get(self.file_url)

    def thumbnail_request(self):
        return self._thread._board._requests_session.get(self.thumbnail_url)

    @property
    def post_url(self):
        board = self._thread._board
        return "%s://%s/%s/res/%i#p%i" % (
            'https' if board._https else 'http',
            _4CHAN_BOARDS_URL,
            board.name,
            self._thread.id,
            self.post_number
        )

    def __repr__(self):
        return "<Post /%s/%i#%i, has_file: %r>" % (
            self._thread._board.name,
            self._thread.id,
            self.post_number,
            self.has_file
        )
