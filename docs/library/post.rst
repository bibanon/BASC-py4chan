:class:`basc_py4chan.Post` – 4chan Post
=======================================

:class:`basc_py4chan.Post` allows for standard access to a 4chan post.

Example
-------

Here is a sample application that grabs and prints :class:`basc_py4chan.Thread` and :class:`basc_py4chan.Post` information:

.. code-block:: python

    # credits to Anarov for improved example
    from __future__ import print_function
    import basc_py4chan

    # get the board we want
    board = basc_py4chan.Board('v')

    # select the first thread on the board
    all_thread_ids = board.get_all_thread_ids()
    first_thread_id = all_thread_ids[0]
    thread = board.get_thread(first_thread_id)

    # print thread information
    print(thread)
    print('Sticky?', thread.sticky)
    print('Closed?', thread.closed)
    print('Replies:', len(thread.replies))

    # print topic post information
    topic = thread.topic
    print('Topic Repr', topic)
    print('Postnumber', topic.post_number)
    print('Timestamp', topic.timestamp)
    print('Datetime', repr(topic.datetime))
    print('Subject', topic.subject)
    print('Comment', topic.comment)
    
    # file information
    for f in first_thread.file_objects():
        print('Filename', f.filename)
        print('  Filemd5hex', f.file_md5_hex)
        print('  Fileurl', f.file_url)
        print('  Thumbnailurl', f.thumbnail_url)
        print()

Basic Usage
-----------

.. autoclass:: basc_py4chan.Post

    Post objects are not instantiated directly, but through a :class:`basc_py4chan.Thread` object with an attribute like :attr:`basc_py4chan.Thread.all_posts`.
