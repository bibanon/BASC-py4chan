#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .url import Url
from .util import clean_comment_body


class Post(object):
    """Represents a 4chan post.

    Attributes:
        post_id (int): ID of this post. Eg: ``123123123``, ``456456456``.
        poster_id (int): Poster ID.
        name (string): Poster's name.
        email (string): Poster's email.
        tripcode (string): Poster's tripcode.
        subject (string): Subject of this post.
        comment (string): This comment, with the <wbr> tag removed.
        html_comment (string): Original, direct HTML of this comment.
        text_comment (string): Plaintext version of this comment.
        is_op (bool): Whether this is the OP (first post of the thread)
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
        url (string): URL of this post.
        semantic_url (string): URL of this post, with the thread's 'semantic' component.
        semantic_slug (string): This post's 'semantic slug'.
    """
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data
        self._url = Url(board=self._thread._board.name, https=thread.https)		# 4chan URL generator

    @property
    def is_op(self):
        return self == self.thread.topic
    is_OP = is_op

    @property
    def post_id(self):
        return self._data.get('no')
    number = num = no = post_number = post_id

    @property
    def poster_id(self):
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
    def html_comment(self):
        return self._data.get('com', '')

    @property
    def text_comment(self):
        return clean_comment_body(self.html_comment)

    @property
    def comment(self):
        return self.html_comment.replace('<wbr>', '')

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
        return self._url.file_url(
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
        return self._url.thumb_url(
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
    def url(self):
        return '%s#p%i' % (self._thread.url, self.post_number)

    @property
    def semantic_url(self):
        return '%s#p%i' % (self._thread.semantic_url, self.post_number)

    @property
    def semantic_slug(self):
        return self._data.get('semantic_url')

    def __repr__(self):
        return '<Post /%s/%i#%i, has_file: %r>' % (
            self._thread._board.name,
            self._thread.id,
            self.post_number,
            self.has_file
        )
