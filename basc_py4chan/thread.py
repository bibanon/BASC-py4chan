#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .post import Post
from .url import Url


class Thread(object):
    """Represents a 4chan thread.

    Attributes:
        closed (bool): Whether the thread has been closed.
        sticky (bool): Whether this thread is a 'sticky'.
        archived (bool): Whether the thread has been archived.
        bumplimit (bool): Whether the thread has hit the bump limit.
        imagelimit (bool): Whether the thread has hit the image limit.
        custom_spoiler (int): Number of custom spoilers in the thread (if the board supports it)
        topic (:class:`basc_py4chan.Post`): Topic post of the thread, the OP.
        posts (list of :class:`basc_py4chan.Post`): List of all posts in the thread, including the OP.
        all_posts (list of :class:`basc_py4chan.Post`): List of all posts in the thread, including the OP and any omitted posts.
        url (string): URL of the thread, not including semantic slug.
        semantic_url (string): URL of the thread, with the semantic slug.
        semantic_slug (string): The 'pretty URL slug' assigned to this thread by 4chan.
    """

    def __init__(self, board, id):
        self._board = board
        self._url = Url(board_name=board.name, https=board.https)  # 4chan URL generator
        self.id = self.number = self.num = self.no = id
        self.topic = self.op = None
        self.replies = []
        self.num_replies = 0
        self.num_images = 0
        self.is_404 = False
        self.last_reply_id = 0
        self.omitted_posts = 0
        self.omitted_images = 0
        self.want_update = False
        self._last_modified = None

    def __len__(self):
        return self.num_replies

    @property
    def _api_url(self):
        return self._url.thread_api_url(self.id)

    @property
    def closed(self):
        return self.topic._data.get('closed') == 1

    @property
    def sticky(self):
        return self.topic._data.get('sticky') == 1

    @property
    def archived(self):
        return self.topic._data.get('archived') == 1

    @property
    def imagelimit(self):
        return self.topic._data.get('imagelimit') == 1

    @property
    def bumplimit(self):
        return self.topic._data.get('bumplimit') == 1

    @property
    def custom_spoiler(self):
        return self.topic._data.get('custom_spoiler', 0)

    @classmethod
    def _from_request(cls, board, res, id):
        if res.status_code == 404:
            return None

        res.raise_for_status()

        return cls._from_json(res.json(), board, id, res.headers['Last-Modified'])

    @classmethod
    def _from_json(cls, json, board, id=None, last_modified=None):
        t = cls(board, id)
        t._last_modified = last_modified

        posts = json['posts']
        head, rest = posts[0], posts[1:]

        t.topic = t.op = Post(t, head)
        t.replies.extend(Post(t, p) for p in rest)

        t.id = head.get('no', id)
        t.num_replies = head['replies']
        t.num_images = head['images']
        t.omitted_images = head.get('omitted_images', 0)
        t.omitted_posts = head.get('omitted_posts', 0)

        if id is not None:
            if not t.replies:
                t.last_reply_id = t.topic.post_number
            else:
                t.last_reply_id = t.replies[-1].post_number

        else:
            t.want_update = True

        return t

    def files(self):
        """Returns the URLs of all files attached to posts in the thread."""
        if self.topic.has_file:
            yield self.topic.file.file_url
        for reply in self.replies:
            if reply.has_file:
                yield reply.file.file_url

    def thumbs(self):
        """Returns the URLs of all thumbnails in the thread."""
        if self.topic.has_file:
            yield self.topic.file.thumbnail_url
        for reply in self.replies:
            if reply.has_file:
                yield reply.file.thumbnail_url

    def filenames(self):
        """Returns the filenames of all files attached to posts in the thread."""
        if self.topic.has_file:
            yield self.topic.file.filename
        for reply in self.replies:
            if reply.has_file:
                yield reply.file.filename

    def thumbnames(self):
        """Returns the filenames of all thumbnails in the thread."""
        if self.topic.has_file:
            yield self.topic.file.thumbnail_fname
        for reply in self.replies:
            if reply.has_file:
                yield reply.file.thumbnail_fname

    def file_objects(self):
        """Returns the :class:`basc_py4chan.File` objects of all files attached to posts in the thread."""
        if self.topic.has_file:
            yield self.topic.file
        for reply in self.replies:
            if reply.has_file:
                yield reply.file

    def update(self, force=False, timeout=None):
        """Fetch new posts from the server.

        Arguments:
            force (bool): Force a thread update, even if thread has 404'd.

        Returns:
            int: How many new posts have been fetched.
        """

        # The thread has already 404'ed, this function shouldn't do anything anymore.
        if self.is_404 and not force:
            return 0

        if self._last_modified:
            headers = {'If-Modified-Since': self._last_modified}
        else:
            headers = None

        # random connection errors, just return 0 and try again later
        try:
            res = self._board._requests_session.get(self._api_url, headers=headers, timeout=timeout)
        except:
            # try again later
            return 0

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

            self._last_modified = res.headers['Last-Modified']
            posts = res.json()['posts']

            original_post_count = len(self.replies)
            self.topic = Post(self, posts[0])

            if self.last_reply_id and not force:
                self.replies.extend(Post(self, p) for p in posts if p['no'] > self.last_reply_id)
            else:
                self.replies[:] = [Post(self, p) for p in posts[1:]]

            new_post_count = len(self.replies)

            # Update replies to indicate if they or their files were deleted. The topic itself is already updated,
            # because it's newly instantiated each time.
            old_replies = {p.post_id: p for p in self.replies}
            new_replies = {p.post_id: p for p in (Post(self, p) for p in posts[1:])}
            for post_id, post in old_replies.items():
                if post_id not in new_replies:
                    post.deleted = True
                    new_post_count -= 1
                    continue

                # Only file deleted can actually change for regular replies
                if 'filedeleted' in post._data:
                    post._data['filedeleted'] = new_replies[post_id]._data['filedeleted']

            post_count_delta = new_post_count - original_post_count
            if not post_count_delta:
                return 0

            self.last_reply_id = self.replies[-1].post_number
            return post_count_delta

        else:
            res.raise_for_status()

    def expand(self, timeout=None):
        """If there are omitted posts, update to include all posts."""
        if self.omitted_posts > 0:
            self.update(timeout=timeout)

    @property
    def posts(self):
        return [self.topic] + self.replies

    @property
    def all_posts(self):
        self.expand()
        return self.posts

    @property
    def https(self):
        return self._board._https

    @property
    def url(self):
        return self._url.thread_url(self.id)

    @property
    def semantic_url(self):
        return '%s/%s' % (self.url, self.semantic_slug)

    @property
    def semantic_slug(self):
        return self.topic.semantic_slug

    def __repr__(self):
        extra = ''
        if self.omitted_images or self.omitted_posts:
            extra = ', %i omitted images, %i omitted posts' % (
                self.omitted_images, self.omitted_posts
            )

        return '<Thread /%s/%i, %i replies%s>' % (
            self._board.name, self.id, len(self.replies), extra
        )
