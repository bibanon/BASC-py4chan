BASC-py4chan
============

The Bibliotheca Anonoma's **complete Python Wrapper for the 4chan API.**
Uses requests, respects if-modified-since headers on updating threads.
Caches thread objects. Fun stuff.

An absolute must if you want to interface with or scrape from 4chan,
using a Python script.

Documentation is located `here <http://basc-py4chan.readthedocs.org/en/latest/index.html>`_, still being written but already quite useful.

`You can install this wrapper library straight from
PyPi <https://pypi.python.org/pypi/BASC-py4chan>`__.

This is the Bibliotheca Anonoma StoryCorps' (BASC) updated fork of
py4chan, based on `Edgeworth's outdated
original. <https://github.com/e000/py-4chan>`__

--------------

If you're a developer that still uses Edgeworth's py-4chan, and are too
lazy to change the function names, the BASC still maintains `an
up-to-date, API compatible version of py-4chan
here. <https://github.com/bibanon/py-4chan>`__

Usage
-----

.. code:: python

    import basc_py4chan
    b = basc_py4chan.Board('b')
    thread = b.get_thread(423491034)

    print thread

    for file in thread.files():
        print file
        
    # In a while...
    print "I fetched", thread.update(), "new replies."

API Documentation coming soon, but for now, figure it out from the
source.

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

