Tutorial
========

When using BASC-py4chan, it can be a bit hard to find where to begin. Here, we run through how to create and use the various objects available in this module.


Boards
------
:mod:`basc_py4chan.Board` is the first thing you create when using BASC-py4chan. Everything else is created through that class. The most basic way to create a board is as below::

    board = basc_py4chan.Board('tg')

This creates a :mod:`basc_py4chan.Board` object that you can then use to create :mod:`basc_py4chan.Thread` and :mod:`basc_py4chan.Post` objects.

But what sort of things does a :mod:`basc_py4chan.Board` object let you do?

Here's a short code snippet of us printing out how many threads are active on a board::

    board = basc_py4chan.Board('tg')
    thread_ids = board.get_all_thread_ids()
    str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
    print('There are', len(all_ids), 'active threads on /tg/:', ', '.join(str_thread_ids))


Threads
-------
Listing how many threads exist on a board is all well and good, but most people want to actually get threads and do things with them. Here, we'll describe how to do that.

All :mod:`basc_py4chan.Thread` objects are created by a :mod:`basc_py4chan.Board` object, using one of the :meth:`basc_py4chan.Board.get_thread` methods.

For this example, we have a user ask us about "thread 1234", and we return information about it::

    thread_id = 1234
    board = basc_py4chan.Board('tg')

    if board.thread_exists(thread_id):
        thread = board.get_thread(thread_id)

        # print thread information
        print('Thread', thread_id)
        if thread.closed:
            print('  is closed')
        if thread.sticky
            print('  is a sticky')

        # information from the OP
        topic = thread.topic
        print('  is named:', topic.subject)
        print('  and was made by:', name, email)
