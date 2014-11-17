import requests

from . import __version__
from .url import URL, CATALOG, ALL_THREADS
from .thread import Thread

def get_boards(board_name_list, *args, **kwargs):
    if isinstance(board_name_list, basestring):
        board_name_list = board_name_list.split()
    return [Board(name, *args, **kwargs) for name in board_name_list]

class Board(object):
    def __init__(self, board_name, https=False, clean_comments=True,
                 api_url=URL['api'], session=None):
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

    def get_thread(self, id, update_if_cached=True):
        """
            Get a thread from 4chan via 4chan API.

            :param id: Thread ID
            :param update_if_cached: Should the thread be updated if it's found in the cache?
            :return: Thread
        """
        if id in self._thread_cache:
            thread = self._thread_cache[id]
            if update_if_cached:
                thread.update()

            return thread

        res = self._requests_session.get(self._thread_path % id)

        thread = Thread._from_request(self, res, id)
        self._thread_cache[id] = thread

        return thread

    def thread_exists(self, id):
        """
            Check if a thread exists, or is 404.
            :param id: Thread ID
            :return: bool
        """
        return self._requests_session.head(self._thread_path % id).ok

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
        """
            Get all threads on a certain page. Pages are now indexed at 1, instead of 0.
            If the thread is already in cache, return cached thread entry.

            Sets thread.want_update to True if the thread is being returned from the cache.
            :param: page: Page to fetch thread from
            :return: list[Thread]
        """
        return self._request_threads(page)

    def get_all_thread_ids(self):
        """
            Return a list of all thread IDs.

            :return: list[int]
        """
        json = self._get_json(ALL_THREADS)
        return [thread['no'] for page in json for thread in page['threads']]

    def get_all_threads(self, expand=False):
        """
            Return all threads on all pages.

            If not expanded, result is same as get_threads run across all board pages,
            with last 3-5 replies included.

            Uses the catalog when not expanding, and uses the flat thread ID listing
            at /{board}/threads.json when expanding for more efficient resource usage.

            If expanded, all data of all threads is returned with no omitted posts.
            :param: expand: Whether or not to expand threads
            :return: list[Thread]
        """
        if not expand:
            return self._request_threads(CATALOG)

        thread_ids = self.get_all_thread_ids()
        threads = [self.get_thread(id) for id in thread_ids]

        return filter(None, threads)

    def refresh_cache(self, if_want_update=False):
        """
            Update all threads currently stored in the cache.
        """
        for thread in self._thread_cache.values():
            if if_want_update:
                if not thread.want_update:
                    continue
            thread.update()

    def clear_cache(self):
        """
            Remove everything currently stored in the cache.
        """
        self._thread_cache.clear()

    @property
    def name(self):
        """
            Board name that this board represents.
            :return: string
        """
        return self._board_name

    def __repr__(self):
        return '<Board /%s/>' % self.name

board = Board
