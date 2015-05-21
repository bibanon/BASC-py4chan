4chan Python Library
====================
The Bibliotheca Anonoma's **complete Python Wrapper for the 4chan API.**
Uses requests, respects if-modified-since headers on updating threads.
Caches thread objects. Fun stuff.

An absolute must if you want to interface with or scrape from 4chan,
using a Python script.

`Hosted Documentation <http://basc-py4chan.readthedocs.org/en/latest/index.html>`_

`Github Repository <https://github.com/bibanon/BASC-py4chan>`_

You can install this library `straight from
PyPi <https://pypi.python.org/pypi/BASC-py4chan>`_ with::

    pip install basc-py4chan


**Getting Help**

If you want help, or you have some trouble using this library, our primary IRC channel
is `#bibanon on irc.rizon.net <http://qchat2.rizon.net/?channels=bibanon>`_. Simply head
in there and talk to dan or antonizoon. Otherwise, you can put a issue on our `Github
Issue Tracker <https://github.com/bibanon/BASC-py4chan>`_ and we'll respond as soon as
we can!

--------

Originally written by `Edgeworth <https://github.com/e000/py-4chan>`_, the library
has been adopted and extended by `Bibliotheca Anonoma <https://github.com/bibanon>`_.

**Note:** If you're a developer that still uses Edgeworth's py-4chan, and don't
want to change the function names, Bibliotheca Anonoma maintains an `up-to-date,
API-compatible version of py-4chan here. <https://github.com/bibanon/py-4chan>`_

Usage
-----

.. code:: python

    import basc_py4chan
    b = basc_py4chan.Board('b')
    thread = b.get_thread(423491034)

    print(thread)

    for file in thread.files():
        print(file)
        
    # In a while...
    print("I fetched", thread.update(), "new replies.")

Documentation is located `here <http://basc-py4chan.readthedocs.org/en/latest/index.html>`_.

Extending this Library
----------------------

There are a wealth of other imageboard APIs that have adopted a similar structure to the 4chan API (such as 8chan/vichan, or 420chan).

So instead of writing a whole new class from scratch, you could inherit and override BASC-py4chan to support them. Here's how:

.. code:: python
    import basc_py4chan
    
    # new site's API URL structure
    URL = {
        'api': 'a.4cdn.org',          # API subdomain
        'boards': 'boards.4chan.org', # HTML subdomain
        'images': 'i.4cdn.org',       # image host
        'thumbs': 't.4cdn.org',       # thumbs host
        'template': {
            'board': '{name}/%s.json',
            'thread': '{name}/thread/%s.json'
        },
         'all_threads': 'threads',             # json entry for threads
         'catalog_dir': 'catalog',             # catalog directory 
         'boards_list': 'https://a.4cdn.org/boards.json' # list of all boards
    }
    
    class Board(basc_py4chan.Board):
        # override the `boards_list` variable with URL struct
        def _fetch_boards_metadata(boards_list=URL['boards_list']):
            super(boards_list)

        # redeclare to use our URL structs
        def __init__(self, board_name, https=False, site_urls=URL, session=None):
           super(board_name, https=False, site_urls=URL, session=None)
           
    class Thread(basc_py4chan.Threads):
        # add your own overrides here, or leave it alone
        pass

    class Post(basc_py4chan.Post):
        # add your own overrides here, or leave it alone
        pass
        
    # note that all classes must be in one file (we recommend py?chan/__init__.py), due to limitations of python's module extend system


From there, just override any methods in classes Board, Thread or Post as necessary. 

Notice that if your imageboard's API does not support a certain feature in the 4chan API, you should have the function return NULL.

License
-------

.. code:: text

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004

     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

      0. You just DO WHAT THE FUCK YOU WANT TO.
