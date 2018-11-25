Changes from the original py4chan
=================================

Since Edgeworth has gone MIA, `The Bibliotheca Anonoma <http://bibanon.org/>`_ has adopted the
project and made the following improvements.

Changes by `antonizoon <https://github.com/antonizoon>`_
--------------------------------------------------------

-  **4chan Link Structure Update** - 4chan has heavily reformed it's
   link structure, finally removing the strange folder structure
   inherited from the Futaba Channel.
-  **4chan cdn Link update** - To save money on bandwidth. 4chan has
   changed it's image/thumbnail/json/css servers to a domain name with
   fewer characters.
-  **Thread Class:** new ``filenames()`` function that return the
   filenames of all files (not thumbnails) in a thread.
-  **Thread Class:** new ``thumbnames()`` function that return the
   filenames of all thumbnails in a thread.

   -  **Post Class:** new ``image_fname`` and ``thumbnail_fname``
      properties, designed for Thread Class ``filenames()`` and
      ``thumbnames()``.

-  **Actual API Documentation** - Real documentation on using the
   py-4chan library is a must. For some people, it is rocket science.


Changes by `Anorov <https://github.com/Anorov/py-4chan>`_
---------------------------------------------------------

-  **Anorov's underscore\_function\_notation** - Even I have to say that
   CamelCase is beginning to suck, so we've adopted Anorov's function
   notation for py4chan. This breaks API compatibility with the original
   py-4chan, but just use find/replace to change your functions.
-  **Break up classes into separate files.** - Makes the code much
   cleaner.
-  Thread Class: ``expand()`` function, used to display omitted posts
   and images. Used by all\_posts().
-  Thread Class: ``semantic_thread_url()`` function, used to obtain
   4chan's new URL format, which tacks on the thread title (obtained
   from ``slug()``).
-  Post Class: ``comment()`` has been modified to use
   ``clean_comment_body()`` when returning a comment. The raw text from
   the 4chan API can still be obtained from ``orig_comment()``.

   -  Util Class: ``clean_comment_body()`` function, which converts all
      HTML tags and entities within 4chan comments into human-readable
      text equivalents.(e.g. ``<br>`` to a newline, ``<a href>`` into a
      raw link)

-  Board Class: ``_get_json()`` function, which dumps the raw JSON from
   the 4chan API.
-  A whole host of new Catalog parsing functions:

   -  Board Class: ``refresh_cache()`` and ``clear_cache()`` - Get the
      latest Catalog of all threads in the board, or clear the current
      cache.
   -  Board Class: ``get_threads(page)`` - Get a list of all threads on
      a certain page. (Pages are now indexed starting from 1).
   -  Board Class: ``get_all_thread_ids()`` - Get a list of all thread
      IDs on the board.
   -  Board Class: ``get_all_threads()`` - Return all threads on all
      pages in the board.


Changes by `Daniel Oaks <https://github.com/DanielOaks>`_
---------------------------------------------------------

- **ReadTheDocs Documentation** - Splitting the documentation out to
  `ReadTheDocs <http://readthedocs.org>`_, using
  `Sphinx <http://sphinx-doc.org/>`_ to generate nice, useful docs!
