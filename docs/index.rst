4chan Python Library
====================
BASC-py4chan is a Python library that gives access to the 4chan API and an object-oriented way to browse and get board and thread information quickly and easily.

Originally written by `Edgeworth <https://github.com/e000/py-4chan>`_, the library has been adopted and extended by `Bibliotheca Anonoma <https://github.com/bibanon>`_.

.. WARNING::
    If you have an old application written to use the original py4chan, `Bibliotheca Anonoma <https://github.com/bibanon>`_ also maintains a `py-4chan fork <https://github.com/bibanon/py-4chan>`_ on legacy support, only to be updated for URL changes without any new features. This fork is also linked to the `original PyPi package <https://pypi.python.org/pypi/py-4chan>`_, and updating py-4chan using pip will give you the latest version of this fork.

    However, we recommend that **all users** switch to BASC-py4chan. This module is more Pythonic, has better support, documentation, and will be gaining new features.

The BASC-py4chan repository is located `on Github <https://github.com/bibanon/BASC-py4chan>`_, where pull requests and issues can be submitted.

We're currently writing up the documentation for this module, so stick with us while we flesh out the library documentation and the rest of it!

.. toctree::
   :maxdepth: 2

   changes
   faq

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   library/board
   library/thread
   library/post
