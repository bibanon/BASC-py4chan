.. force line break
.. |br| raw:: html

   <br />

4chan Python Library
====================
The Bibliotheca Anonoma's **complete Python Wrapper for the 4chan API.**
Uses requests, respects if-modified-since headers on updating threads.
Caches thread objects. Fun stuff.

An absolute must if you want to interface with or scrape from 4chan,
using a Python script.

`Hosted Documentation <http://basc-py4chan.readthedocs.org/en/latest/index.html>`_

You can install this library `straight from
PyPi <https://pypi.python.org/pypi/BASC-py4chan>`_ with::

    pip install basc-py4chan

The BASC-py4chan repository is located `on Github <https://github.com/bibanon/BASC-py4chan>`_,
where pull requests and issues can be submitted.


**Getting Help** |br|
If you want help, or you have some trouble using this library, our primary IRC channel
is `#bibanon on irc.rizon.net <http://qchat2.rizon.net/?channels=bibanon>`_. Simply head
in there and talk to dan or antonizoon. Otherwise, you can put a issue on our
`Github Issue Tracker <https://github.com/bibanon/BASC-py4chan>`_ and we'll respond as
soon as we can!

--------

Originally written by `Edgeworth <https://github.com/e000/py-4chan>`_, the
library has been adopted and extended by `Bibliotheca Anonoma <https://github.com/bibanon>`_.

**Note:** If you're a developer that still uses Edgeworth's py-4chan, and don't
want to change the function names, Bibliotheca Anonoma maintains an `up-to-date,
API-compatible version of py-4chan here. <https://github.com/bibanon/py-4chan>`_

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

Documentation is located `here <http://basc-py4chan.readthedocs.org/en/latest/index.html>`_.

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
