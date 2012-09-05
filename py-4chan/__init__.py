"""
    py-4chan
    ~~~~~~~~

    Python Wrappers to access 4chan's API.

"""
import requests
import json
from datetime import datetime
import base64

_4CHAN_API = 'api.4chan.org'
_4CHAN_IMAGES_URL = 'images.4chan.org'
_THREAD = '%s/res/%i.json'

class Board(object):
    def __init__(self, boardName, https = False, apiUrl = _4CHAN_API):
        self._https = https
        self._baseUrl = ('http://' if not https else 'https://') + apiUrl
        self._boardName = boardName
        self._requestsSession = requests.session()
        self._threadCache = {}

    def getThread(self, id, updateIfCached = True):
        if id in self._threadCache:
            thread = self._threadCache[id]
            if updateIfCached:
                thread.update()

            if thread.is_404:
                del self._threadCache[id]

            return thread

        try:
            url = '%s/%s' % (self._baseUrl, _THREAD % (self._boardName, id))
            res = self._requestsSession.get(url)

            thread = Thread.fromRequest(self, res, id)
            self._threadCache[id] = thread

            return thread

        except:
            raise

    @property
    def name(self):
        return self._boardName


class Thread(object):
    def __init__(self, board, id):
        self._board = board
        self.id = id
        self.topic = None
        self.replies = []
        self.is_404 = False

    @property
    def Closed(self):
        return self.topic._data['closed'] == 1

    @property
    def Sticky(self):
        return self.topic._data['sticky'] == 1

    @staticmethod
    def fromRequest(board, res, id):
        t = Thread(board, id)
        posts = json.loads(res.text)['posts']
        t.topic = Post.fromDict(t, posts[0])
        t.replies.extend(Post.fromDict(t, p) for p in posts[1:])
        return t

    def update(self):
        """
            Fetch new posts from the server. Returns an integer with the number of new posts.
        """
        pass

    def __repr__(self):
        return '<Thread /%s/%i, %i replies>' % (
            self._board.name, self.id, len(self.replies)
        )


class Post(object):
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data

    @property
    def Id(self):
        return self._data['no']

    @property
    def Timestamp(self):
        return self._data['time']

    @property
    def Datetime(self):
        return datetime.fromtimestamp(self._data['time'])

    @property
    def FileMd5(self):
        return base64.b64decode(self._data['md5'])

    @property
    def FileMd5Hex(self):
        return self.FileMd5.encode('hex')

    @property
    def FileUrl(self):
        board = self._thread._board
        return '%s://%s/%s/src/%i%s' % (
            'https' if board._https else 'http',
            _4CHAN_IMAGES_URL,
            board.name,
            self._data['tim'],
            self._data['ext']
        )

    @staticmethod
    def fromDict(thread, data):
        p = Post(thread, data)
        return p



if __name__ == '__main__':
    v = Board('v')
    thread = v.getThread(152900882)
    print thread
    print thread.Sticky
    print thread.Closed
    topic = thread.topic
    print topic.Timestamp
    print topic.Datetime
    print topic.FileMd5Hex
    print topic.FileUrl
