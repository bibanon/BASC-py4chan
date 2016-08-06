#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .url import Url
from .file import File
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
        is_op (bool): Whether this is the OP (first post of the thread).
        spoiler (bool): Whether the attached file is spoiled.
        timestamp (int): Unix timestamp for this post.
        datetime (:class:`datetime.datetime`): Datetime time of this post.
        first_file (:class:`py8chan.File`): The File object associated with this post.
        has_file (bool): Whether this post has a file attached to it.
        url (string): URL of this post.
        semantic_url (string): URL of this post, with the thread's 'semantic' component.
        semantic_slug (string): This post's 'semantic slug'.
    """
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data
        self._url = Url(board_name=self._thread._board.name, https=thread.https)		# 4chan URL generator

        # add file objects if they exist
        if self.has_file:
            self.file1 = File(self, self._data)

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
    def spoiler(self):
        return self._data.get('spoiler') == 1

    """
        Legacy undocumented compatibility wrappers for File attributes that will be depreciated eventually. 
        We strongly recommend users to use the `Post.file` property instead, which gives you a whole File object that has all the attributes.
    """
    @property
    def file_md5(self):
        if not self.has_file:
            return None

        return self.file1.file_md5

    @property
    def file_md5_hex(self):
        if not self.has_file:
            return None

        return self.file1.file_md5_hex

    @property
    def filename(self):
        if not self.has_file:
            return None

        board = self._thread._board
        
        return self.file1.filename

    @property
    def file_url(self):
        if not self.has_file:
            return None

        board = self._thread._board
        return self.file1.file_url

    @property
    def file_extension(self):
        return self.file1.file_extension

    @property
    def file_size(self):
        return self.file1.file_size

    @property
    def file_width(self):
        return self.file1.file_width

    @property
    def file_height(self):
        return self.file1.file_width

    @property
    def file_deleted(self):
        return self.file1.file_deleted

    @property
    def thumbnail_width(self):
        return self.file1.thumbnail_width

    @property
    def thumbnail_height(self):
        return self.thumbnail_height

    @property
    def thumbnail_fname(self):
        if not self.has_file:
            return None

        return self.file1.thumbnail_fname

    @property
    def thumbnail_url(self):
        if not self.has_file:
            return None

        return self.file1.thumbnail_url

    def file_request(self):
        return self._thread._board._requests_session.get(self.file_url)

    def thumbnail_request(self):
        return self._thread._board._requests_session.get(self.thumbnail_url)

    """New File object properties."""
    @property
    def file(self):
        """
            Returns the File object associated with this post. 
            Currently 4chan only supports one file per post, but 8chan supports multiple,
        """
        if not self.has_file:
            return None
        
        return self.file1

    @property
    def has_file(self):
        return 'filename' in self._data

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
