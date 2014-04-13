BASC py4chan
============

Python Wrapper for 4chan API. Uses requests, respects if-modified-since headers on updating threads. Caches thread objects. Fun stuff.

### Sample Usage

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

API Documentation coming soon, but you can figure most of it out from the source. It's not rocket science.

[You can install this package straight from PyPi](https://pypi.python.org/pypi/py-4chan).

## BASC py4chan 0.3 Update

The Bibliotheca Anonoma StoryCorps has created it's own fork of py-4chan

* **4chan cdn Link update** - To save money on bandwidth. 4chan has changed it's image/thumbnail/json/css servers to a domain name with fewer characters. However, that requires us to update py-4chan links, and that has not been done yet.
* **Anorov's underscore_function_notation** - Even I have to say that CamelCase is beginning to suck. However, you will have to rename all your function calls for existing apps, but that's just a find/replace away.
* **Renamed files() to images(), and any `files` property to `images`** - 4chan only hosts image files, so the name of this function gets confusing, since it can refer to either images thumbnails. The `has_file` and `file_deleted` property retains it's name, though, since it refers to both thumbs and images. 
* **images() and thumbs()** - now return images instead of URLs. The original functions have been renamed to image_urls() and thumb_urls()
* **Post Class: image_fname and thumbnail_fname property**
* **Actual API Documentation** - Real documentation on using the py-4chan library is a must. For some people, it is rocket science.

# License

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