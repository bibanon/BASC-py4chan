.. force line break
.. |br| raw:: html

   <br />

4chan Python Library
====================
*BASC-py4chan* is a Python library that gives access to the 4chan API and an object-oriented way to browse and get board and thread information quickly and easily.

Originally written by `Edgeworth <https://github.com/e000/py-4chan>`_, the library has been adopted and extended by `Bibliotheca Anonoma <https://github.com/bibanon>`_.

.. WARNING::
    If you have an old application written to use the original py4chan, `Bibliotheca Anonoma <https://github.com/bibanon>`_ also maintains a `py-4chan fork <https://github.com/bibanon/py-4chan>`_ on legacy support, only to be updated for URL changes without any new features. This fork is also linked to the `original PyPi package <https://pypi.python.org/pypi/py-4chan>`_, and updating py-4chan using pip will give you the latest version of this fork.

    However, we recommend that **all users** switch to the new BASC-py4chan. This module is more Pythonic, has better support, documentation, and will be gaining new features.

The BASC-py4chan repository is located `on Github <https://github.com/bibanon/BASC-py4chan>`_, where pull requests and issues can be submitted.


**Getting Help** |br|
If you want help, or you have some trouble using this library, our primary IRC channel is `#bibanon on irc.rizon.net <http://qchat2.rizon.net/?channels=bibanon>`_. Simply head in there and talk to dan or antonizoon. Otherwise, you can put a issue on our `Github Issue Tracker <https://github.com/bibanon/BASC-py4chan>`_ and we'll respond as soon as we can!


General Documentation
---------------------

.. toctree::
    :maxdepth: 2

    tutorial
    changes
    faq


API Documentation
-----------------

.. toctree::
    :maxdepth: 2

    library/py4chan
    library/board
    library/thread
    library/post
    library/file
