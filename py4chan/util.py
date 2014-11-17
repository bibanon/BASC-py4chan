"""
    Utility functions.
"""

import re
from HTMLParser import HTMLParser

_parser = HTMLParser()

def clean_comment_body(body):
    """
        Convert all HTML tags and entities within 4chan comments
        into human-readable text equivalents.
    """
    body = _parser.unescape(body)
    body = re.sub(r'<a [^>]+>(.+?)</a>', r'\1', body)
    body = body.replace('<br>', '\n')
    body = re.sub(r'<.+?>', '', body)
    return body
