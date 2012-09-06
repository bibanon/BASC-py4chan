py-4chan
========

Python Wrapper for 4chan API. Uses requests, respects if-modified-since headers on updating threads. Caches thread objects. Fun stuff.

### Sample Usage

``` python
import py4chan
b = py4chan.Board('b')
thread = b.getThread(423491034)

print thread

for file in thread.Files():
    print file
    
# In a while...
print "I fetched," thread.update(), "new replies."
```

API Documentation coming soon, but you can figure most of it out from the source. It's not rocket science.