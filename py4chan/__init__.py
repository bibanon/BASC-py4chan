"""
    py-4chan
    ~~~~~~~~

    Python Wrappers to access 4chan's API.

"""
import requests
from datetime import datetime
import base64

_4CHAN_API = 'api.4chan.org'
_4CHAN_IMAGES_URL = 'images.4chan.org'
_4CHAN_THUMBS_URL = '0.thumbs.4chan.org'
_THREAD = '%s/res/%i.json'
_VERSION = '0.1.1'

class Board(object):
    def __init__(self, boardName, https = False, apiUrl = _4CHAN_API):
        self._https = https
        self._baseUrl = ('http://' if not https else 'https://') + apiUrl
        self._boardName = boardName
        self._requestsSession = requests.session(headers = {'User-Agent': 'py-4chan/%s' % _VERSION})
        self._threadCache = {}

    def getThread(self, id, updateIfCached = True):
        if id in self._threadCache:
            thread = self._threadCache[id]
            if updateIfCached:
                thread.update()

            if thread.is_404:
                del self._threadCache[id]

            return thread

        url = '%s/%s' % (self._baseUrl, _THREAD % (self._boardName, id))
        res = self._requestsSession.get(url)

        thread = Thread.fromRequest(self, res, id)
        self._threadCache[id] = thread

        return thread

    def threadExists(self, id):
        url = '%s/%s' % (self._baseUrl, _THREAD % (self._boardName, id))
        return self._requestsSession.head(url).status_code == 200

    @property
    def Name(self):
        return self._boardName


class Thread(object):
    def __init__(self, board, id):
        self._board = board
        self.id = id
        self.topic = None
        self.replies = []
        self.is_404 = False
        self.last_reply_id = 0
        self._last_modified = None

    @property
    def Closed(self):
        return self.topic._data['closed'] == 1

    @property
    def Sticky(self):
        return self.topic._data['sticky'] == 1

    @staticmethod
    def fromRequest(board, res, id):
        if res.status_code == 404:
            return None

        elif res.status_code == 200:
            t = Thread(board, id)
            t._last_modified = res.headers['last-modified']

            posts = res.json['posts']
            t.topic = Post(t, posts[0])
            t.replies.extend(Post(t, p) for p in posts[1:])

            if not t.replies:
                t.last_reply_id = t.topic.PostNumber
            else:
                t.last_reply_id = t.replies[-1].PostNumber

            return t

        else:
            res.raise_for_status()

    def Files(self):
        """
            Returns a generator that yields all the URL of all the files in the thread.
        """
        yield self.topic.FileUrl
        for reply in self.replies:
            if reply.HasFile:
                yield reply.FileUrl

    def update(self):
        """
            Fetch new posts from the server. Returns an integer with the number of new posts.
        """
        if self.is_404:
            return 0

        url = '%s/%s' % (self._board._baseUrl, _THREAD % (self._board._boardName, self.id))
        res = self._board._requestsSession.get(url, headers = {
            'If-Modified-Since': self._last_modified
        })

        if res.status_code == 304:
            return 0

        elif res.status_code == 404:
            self.is_404 = True
            return 0

        elif res.status_code == 200:
            self._last_modified = res.headers['last-modified']
            posts = res.json['posts']

            originalPostCount = len(self.replies)
            self.replies.extend(Post(self, p) for p in posts if p['no'] > self.last_reply_id)
            newPostCount = len(self.replies)
            postCountDelta = newPostCount - originalPostCount
            if not postCountDelta:
                return 0

            self.last_reply_id = self.replies[-1].PostNumber

            return postCountDelta

        else:
            res.raise_for_status()

    def __repr__(self):
        return '<Thread /%s/%i, %i replies>' % (
            self._board.Name, self.id, len(self.replies)
        )


class Post(object):
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data

    @property
    def PostNumber(self):
        return self._data['no']

    @property
    def Id(self):
        return self._data.get('id')

    @property
    def Name(self):
        return self._data['name'] or None

    @property
    def EMail(self):
        return self._data['email'] or None

    @property
    def Tripcode(self):
        return self._data['tripcode'] or None

    @property
    def Subject(self):
        return self._data['sub'] or None
    
    @property
    def Comment(self):
        return self._data['com'] or None

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
        return self._thread._board._requestsSession.get(self.FileUrl)

    def ThumbnailRequest(self):
        return self._thread._board._requestsSession.get(self.ThumbnailUrl)

    def __repr__(self):
        return "<Post /%s/%i#%i, hasFile: %r>" % (
            self._thread._board.Name,
            self._thread.id,
            self.PostNumber,
            self.HasFile
        )
