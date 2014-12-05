import requests

from . import __version__
from .url import URL, CATALOG, ALL_THREADS
from .thread import Thread

def get_boards(board_name_list, *args, **kwargs):
    if isinstance(board_name_list, basestring):
        board_name_list = board_name_list.split()
    return [Board(name, *args, **kwargs) for name in board_name_list]

class Board(object):
    """Represents a 4chan board.

    Attributes:
        name (str): Name of this board, such as ``tg`` or ``k``
    """
    def __init__(self, board_name, https=False, clean_comments=True,
                 api_url=URL['api'], session=None):
        """Creates a :mod:`basc_py4chan.Board` object.

        Args:
            board_name (string): Name of the board, such as "tg" or "etc".
            https (bool): Whether to use a secure connection to 4chan.
            clean_comments (bool): Whether post objects will try to parse HTML comments
                (HTML entities, tags and links) into "cleaned" plaintext.
            api_url: Base 4chan API URL. This will be automatically set in all cases.
            session: Existing requests.session object to use instead of our current one.
        """
        self._board_name = board_name
        self._protocol = 'https://' if https else 'http://'
        self._clean_comments = clean_comments
        self._base_url = self._protocol + api_url

        self._requests_session = session or requests.session()
        self._requests_session.headers['User-Agent'] = 'py-4chan/%s' % __version__

        self._board_path = '%s/%s' % (self._base_url,
                                      URL['template']['board'].format(name=board_name))
        self._thread_path = '%s/%s' % (self._base_url,
                                       URL['template']['thread'].format(name=board_name))

        self._thread_cache = {}

    def _get_json(self, path):
        res = self._requests_session.get(self._board_path % path)
        res.raise_for_status()
        return res.json()

    def get_thread(self, thread_id, update_if_cached=True):
        """Get a thread from 4chan via 4chan API.

        Args:
            thread_id (int): Thread ID
            update_if_cached (bool): Whether the thread should be updated if it's already in our cache

        Returns:
            :class:`basc_py4chan.Thread`: Thread object
        """
        if thread_id in self._thread_cache:
            thread = self._thread_cache[thread_id]
            if update_if_cached:
                thread.update()

            return thread

        res = self._requests_session.get(self._thread_path % thread_id)

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
        return self._requests_session.head(self._thread_path % thread_id).ok

    def _catalog_to_threads(self, json):
        threads_json = [thread for page in json for thread in page['threads']]
        thread_list = [{'posts': [thread] + thread.get('last_replies', [])}
                       for thread in threads_json]

        for thread in thread_list:
            thread['posts'][0].pop('last_replies', None)

        return thread_list

    def _request_threads(self, page):
        json = self._get_json(page)

        if page == CATALOG:
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
        return self._request_threads(page)

    def get_all_thread_ids(self):
        """Return the ID of every thread on this board.

        Returns:
            list of ints: List of IDs of every thread on this board.
        """
        json = self._get_json(ALL_THREADS)
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
            return self._request_threads(CATALOG)

        thread_ids = self.get_all_thread_ids()
        threads = [self.get_thread(id) for id in thread_ids]

        return filter(None, threads)

    def refresh_cache(self, if_want_update=False):
        """Update all threads currently stored in our cache."""
        for thread in self._thread_cache.values():
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

    def __repr__(self):
        return '<Board /%s/>' % self.name

board = Board
