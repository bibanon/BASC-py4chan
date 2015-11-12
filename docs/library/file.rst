:class:`basc_py4chan.File` – 4chan File
=======================================

:class:`basc_py4chan.Post` allows for standard access to a 4chan file. This provides programs with a complete File object that contains all metadata about the 4chan file, and makes migration easy if 4chan ever makes multiple files in one Post possible (as 8chan does).

Basic Usage
-----------

.. autoclass:: basc_py4chan.File

    File objects are not instantiated directly, but through a :class:`basc_py4chan.File` object with an attribute like :attr:`basc_py4chan.Post.first_file`.