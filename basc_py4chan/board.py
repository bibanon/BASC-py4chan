#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from . import __version__
from .thread import Thread
from .url import Url

# cached metadata for boards
_metadata = {}

# compatibility layer for Python2's `basestring` variable
# http://www.rfk.id.au/blog/entry/preparing-pyenchant-for-python-3/
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = str, bytes
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


def _fetch_boards_metadata(url_generator):
    if not _metadata:
        resp = requests.get(url_generator.board_list())
        resp.raise_for_status()
        data = {entry['board']: entry for entry in resp.json()['boards']}
        _metadata.update(data)


def _get_board_metadata(url_generator, board, key):
    _fetch_boards_metadata(url_generator)
    return _metadata[board][key]


def get_boards(board_name_list, *args, **kwargs):
    """Given a list of boards, return :class:`basc_py4chan.Board` objects.

    Args:
        board_name_list (list): List of board names to get, eg: ['b', 'tg']

    Returns:
        dict of :class:`basc_py4chan.Board`: Requested boards.
    """
    if isinstance(board_name_list, basestring):
        board_name_list = board_name_list.split()
    return [Board(name, *args, **kwargs) for name in board_name_list]


def get_all_boards(*args, **kwargs):
    """Returns every board on 4chan.

    Returns:
        dict of :class:`basc_py4chan.Board`: All boards.
    """
    # Use https based on how the Board class instances are to be instantiated
    https = kwargs.get('https', args[1] if len(args) > 1 else False)

    # Dummy URL generator, only used to generate the board list which doesn't
    # require a valid board name
    url_generator = Url(None, https)
    _fetch_boards_metadata(url_generator)
    return get_boards(_metadata.keys(), *args, **kwargs)


class Board(object):
    """Represents a 4chan board.

    Attributes:
        name (str): Name of this board, such as ``tg`` or ``k``.
        name (string): Name of the board, such as "tg" or "etc".
        title (string): Board title, such as "Animu and Mango".
        is_worksafe (bool): Whether this board is worksafe.
        page_count (int): How many pages this board has.
        threads_per_page (int): How many threads there are on each page.
    """
    def __init__(self, board_name, https=False, session=None):
        """Creates a :mod:`basc_py4chan.Board` object.

        Args:
            board_name (string): Name of the board, such as "tg" or "etc".
            https (bool): Whether to use a secure connection to 4chan.
            session: Existing requests.session object to use instead of our current one.
        """
        self._board_name = board_name
        self._https = https
        self._protocol = 'https://' if https else 'http://'
        self._url = Url(board=board_name, https=self._https)

        self._requests_session = session or requests.session()
        self._requests_session.headers['User-Agent'] = 'py-4chan/%s' % __version__

        self._thread_cache = {}

    def _get_metadata(self, key):
        return _get_board_metadata(self._url, self._board_name, key)

    def _get_json(self, url):
        res = self._requests_session.get(url)
        res.raise_for_status()
        return res.json()

    def get_thread(self, thread_id, update_if_cached=True, raise_404=False):
        """Get a thread from 4chan via 4chan API.

        Args:
            thread_id (int): Thread ID
            update_if_cached (bool): Whether the thread should be updated if it's already in our cache
            raise_404 (bool): Raise an Exception if thread has 404'd

        Returns:
            :class:`basc_py4chan.Thread`: Thread object
        """
        # see if already cached
        cached_thread = self._thread_cache.get(thread_id)
        if cached_thread:
            if update_if_cached:
                cached_thread.update()
            return cached_thread

        res = self._requests_session.get(
            self._url.thread_api_url(
                thread_id = thread_id
                )
        )

        # check if thread exists
        if raise_404:
            res.raise_for_status()
        elif not res.ok:
            return None

        thread = Thread._from_request(self, res, thread_id)
        self._thread_cache[thread_id] = thread

        return thread

    def thread_exists(self, thread_id):
        """Check if a thread exists or has 404'd.

        Args:
            thread_id (int): Thread ID

        Returns:
            bool: Whether the given thread exists on this board.
        """
        return self._requests_session.head(
            self._url.thread_api_url(
                thread_id=thread_id
                )
        ).ok

    def _catalog_to_threads(self, json):
        threads_json = [thread for page in json for thread in page['threads']]
        thread_list = [{'posts': [thread] + thread.get('last_replies', [])}
                       for thread in threads_json]

        for thread in thread_list:
            thread['posts'][0].pop('last_replies', None)

        return thread_list

    def _request_threads(self, url):
        json = self._get_json(url)

        if url == self._url.catalog():
            thread_list = self._catalog_to_threads(json)
        else:
            thread_list = json['threads']

        threads = []
        for thread_json in thread_list:
            id = thread_json['posts'][0]['no']
            if id in self._thread_cache:
                thread = self._thread_cache[id]
                thread.want_update = True
            else:
                thread = Thread._from_json(thread_json, self)
                self._thread_cache[thread.id] = thread

            threads.append(thread)

        return threads

    def get_threads(self, page=1):
        """Returns all threads on a certain page.

        Gets a list of Thread objects for every thread on the given page. If a thread is
        already in our cache, the cached version is returned and thread.want_update is
        set to True on the specific thread object.

        Pages on 4chan are indexed from 1 onwards.

        Args:
            page (int): Page to request threads for. Defaults to the first page.

        Returns:
            list of :mod:`basc_py4chan.Thread`: List of Thread objects representing the threads on the given page.
        """
        url = self._url.page_url(page)
        return self._request_threads(url)

    def get_all_thread_ids(self):
        """Return the ID of every thread on this board.

        Returns:
            list of ints: List of IDs of every thread on this board.
        """
        json = self._get_json(self._url.thread_list())
        return [thread['no'] for page in json for thread in page['threads']]

    def get_all_threads(self, expand=False):
        """Return every thread on this board.

        If not expanded, result is same as get_threads run across all board pages,
        with last 3-5 replies included.

        Uses the catalog when not expanding, and uses the flat thread ID listing
        at /{board}/threads.json when expanding for more efficient resource usage.

        If expanded, all data of all threads is returned with no omitted posts.

        Args:
            expand (bool): Whether to download every single post of every thread.
                If enabled, this option can be very slow and bandwidth-intensive.

        Returns:
            list of :mod:`basc_py4chan.Thread`: List of Thread objects representing every thread on this board.
        """
        if not expand:
            return self._request_threads(self._url.catalog())

        thread_ids = self.get_all_thread_ids()
        threads = [self.get_thread(id, raise_404=False) for id in thread_ids]

        return filter(None, threads)

    def refresh_cache(self, if_want_update=False):
        """Update all threads currently stored in our cache."""
        for thread in tuple(self._thread_cache.values()):
            if if_want_update:
                if not thread.want_update:
                    continue
            thread.update()

    def clear_cache(self):
        """Remove everything currently stored in our cache."""
        self._thread_cache.clear()

    @property
    def name(self):
        return self._board_name

    @property
    def title(self):
        return self._get_metadata('title')

    @property
    def is_worksafe(self):
        if self._get_metadata('ws_board'):
            return True
        return False

    @property
    def page_count(self):
        return self._get_metadata('pages')

    @property
    def threads_per_page(self):
        return self._get_metadata('per_page')

    @property
    def https(self):
        return self._https

    def __repr__(self):
        return '<Board /%s/>' % self.name

board = Board
