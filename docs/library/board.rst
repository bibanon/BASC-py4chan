:class:`basc_py4chan.Board` – 4chan Boards
==========================================

:class:`basc_py4chan.Board` provides access to a 4chan board including checking if threads exist, retrieving appropriate :class:`basc_py4chan.Thread` objects, and returning lists of all the threads that exist on the given board.

Example
-------

Here is a sample application that grabs and uses Board information::

    from __future__ import print_function
    import basc_py4chan

    board = basc_py4chan.Board('tg')
    thread_ids = board.get_all_thread_ids()
    str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
    print('There are', len(all_ids), 'active threads on /tg/:', ', '.join(str_thread_ids))

Basic Usage
-----------

.. autoclass:: basc_py4chan.Board

Methods
-------

    .. automethod:: basc_py4chan.Board.__init__

    .. automethod:: basc_py4chan.Board.thread_exists

    .. automethod:: basc_py4chan.Board.get_thread

    .. automethod:: basc_py4chan.Board.get_threads

    .. automethod:: basc_py4chan.Board.get_all_threads

    .. automethod:: basc_py4chan.Board.get_all_thread_ids

    .. automethod:: basc_py4chan.Board.refresh_cache

    .. automethod:: basc_py4chan.Board.clear_cache
