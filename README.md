BASC py4chan
============

Python Wrapper for 4chan API. Uses requests, respects if-modified-since headers on updating threads. Caches thread objects. Fun stuff.

[You can install this wrapper library straight from PyPi](https://pypi.python.org/pypi/BASC-py4chan).

This is the Bibliotheca Anonoma StoryCorps' (BASC) updated fork of py4chan, based on [Edgeworth's outdated original.](https://github.com/e000/py-4chan) 

## Changelog

Since Edgeworth has gone MIA, the BASC has adopted the project and made the following improvements.

* Made by [antonizoon](https://github.com/antonizoon):
  * **4chan Link Structure Update** - 4chan has heavily reformed it's link structure, finally removing the strange folder structure inherited from the Futaba Channel.
  * **4chan cdn Link update** - To save money on bandwidth. 4chan has changed it's image/thumbnail/json/css servers to a domain name with fewer characters.
  * **Thread Class:** new `filenames()` function that return the filenames of all files (not thumbnails) in a thread.
  * **Thread Class:** new `thumbnames()` function that return the filenames of all thumbnails in a thread.
    * **Post Class:** new `image_fname` and `thumbnail_fname` properties, designed for Thread Class `filenames()` and `thumbnames()`.
  * **Actual API Documentation** - Real documentation on using the py-4chan library is a must. For some people, it is rocket science.
* Made by [Anorov](https://github.com/Anorov/py-4chan):
  * **Anorov's underscore_function_notation** - Even I have to say that CamelCase is beginning to suck, so we've adopted Anorov's function notation for py4chan. This breaks API compatibility with the original py-4chan, but just use find/replace to change your functions.
  * **Break up classes into separate files.** - Makes the code much cleaner.

If you're a developer that still uses Edgeworth's py-4chan, and are too lazy to change the function names, the BASC still maintains [an up-to-date, API compatible version of py-4chan here.](https://github.com/bibanon/py-4chan)

## Usage

``` python
import py4chan
b = py4chan.Board('b')
thread = b.get_thread(423491034)

print thread

for file in thread.files():
    print file
    
# In a while...
print "I fetched", thread.update(), "new replies."
```

API Documentation coming soon, but for now, figure it out from the source.

## License

``` text
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

```