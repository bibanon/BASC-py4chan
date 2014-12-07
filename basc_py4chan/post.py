from datetime import datetime

from .url import URL
from .util import clean_comment_body

class Post(object):
    """Represents a 4chan post.

    Attributes:
        post_number (int): Number of this post relative to the thread. Eg: ``4``, ``6``, ``7``, ``8``.
        id (int): Post ID.
        name (string): Poster's name.
        email (string): Poster's email.
        tripcode (string): Poster's tripcode.
        subject (string): Subject of this post.
        orig_comment (string): Original, direct HTML of this comment.
        comment (string): Comment data, either cleaned or not depending.
        timestamp (int): Unix timestamp for this post.
        datetime (:class:`datetime.datetime`): Datetime time of this post.
        file_md5 (string): MD5 hash of the file attached to this post.
        file_md5_hex (string): Hex-encoded MD5 hash of the file attached to this post.
        filename (string): Original name of the file attached to this post.
        file_url (string): URL of the file attached to this post.
        file_extension (string): Extension of the file attached to this post. Eg: ``png``, ``webm``, etc.
        file_size (int): Size of the file attached to this post.
        file_width (int): Width of the file attached to this post.
        file_height (int): Height of the file attached to this post.
        file_deleted (bool): Whether the file attached to this post was deleted after being posted.
        thumbnail_width (int): Width of the thumbnail attached to this post.
        thumbnail_height (int): Height of the thumbnail attached to this post.
        thumbnail_fname (string): Filename of the thumbnail attached to this post.
        thumbnail_url (string): URL of the thumbnail attached to this post.
        has_file (bool): Whether this post has a file attached to it.
        post_url (string): URL of this post.
    """
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data
        self._clean_comments = thread._board._clean_comments

    @property
    def post_number(self):
        return self._data.get('no')
    number = num = no = post_number

    @property
    def id(self):
        return self._data.get('id')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def email(self):
        return self._data.get('email')

    @property
    def tripcode(self):
        return self._data.get('trip')

    @property
    def subject(self):
        return self._data.get('sub')

    @property
    def orig_comment(self):
        return self._data.get('com', '')
    html_comment = orig_comment

    @property
    def comment(self):
        if not self._clean_comments or not self.orig_comment:
            return self.orig_comment

        if 'cleaned_comment' not in self._data:
            self._data['cleaned_comment'] = clean_comment_body(self.orig_comment)

        return self._data['cleaned_comment']
    body = text = comment

    @property
    def timestamp(self):
        return self._data['time']

    @property
    def datetime(self):
        return datetime.fromtimestamp(self._data['time'])

    @property
    def file_md5(self):
        if not self.has_file:
            return None

        return self._data['md5'].decode('base64')

    @property
    def file_md5_hex(self):
        if not self.has_file:
            return None

        return self.file_md5.encode('hex')

    @property
    def filename(self):
        if not self.has_file:
            return None

        board = self._thread._board
        
        return '%i%s' % (
            self._data['tim'],
            self._data['ext']
        )

    @property
    def file_url(self):
        if not self.has_file:
            return None

        board = self._thread._board
        return '%s%s/%s/%i%s' % (
            board._protocol,
            URL['images'],
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
        return self._data.get('filedeleted') == 1

    @property
    def thumbnail_width(self):
        return self._data.get('tn_w')

    @property
    def thumbnail_height(self):
        return self._data.get('tn_h')

    @property
    def thumbnail_fname(self):
        if not self.has_file:
            return None

        board = self._thread._board

        return '%is.jpg' % (
            self._data['tim']
        )

    @property
    def thumbnail_url(self):
        if not self.has_file:
            return None

        board = self._thread._board
        return '%s%s/%s/%is.jpg' % (
            board._protocol,
            URL['thumbs'],
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
    def _semantic_url(self):
        return self._data.get('semantic_url')

    @property
    def post_url(self):
        return '%s#p%i' % (self._thread.thread_url, self.post_number)
    url = post_url

    def __repr__(self):
        return '<Post /%s/%i#%i, has_file: %r>' % (
            self._thread._board.name,
            self._thread.id,
            self.post_number,
            self.has_file
        )
