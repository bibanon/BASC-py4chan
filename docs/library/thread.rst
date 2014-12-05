:class:`basc_py4chan.Thread` – Access to 4chan Boards
==================================================

:class:`basc_py4chan.Thread` allows for standard access to a 4chan board, including checking if threads exist, retrieving appropriate :class:`basc_py4chan.Board` objects, and returning lists of all the threads that exist on the given board.

Here is a sample application that grabs and uses Board information, :file:`example.py`::

    from __future__ import print_function
    import basc_py4chan

    board = basc_py4chan.Board('tg')
    str_thread_ids = [str(id) for id in board.get_all_thread_ids()]
    print('Active threads on /tg/:', ', '.join(str_thread_ids))


.. autoclass:: basc_py4chan.Thread

    Thread objects are not instantiated directly, but instead through the appropriate :class:`basc_py4chan.Board` methods such as :meth:`basc_py4chan.Board.get_thread`.

    .. automethod:: basc_py4chan.Thread.files

    .. automethod:: basc_py4chan.Thread.thumbs

    .. automethod:: basc_py4chan.Thread.filenames

    .. automethod:: basc_py4chan.Thread.thumbnames

    .. automethod:: basc_py4chan.Thread.update

    .. automethod:: basc_py4chan.Thread.expand
