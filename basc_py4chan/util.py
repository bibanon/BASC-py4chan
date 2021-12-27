#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility functions."""

import re
import html

_parser = html


def clean_comment_body(body):
    """Returns given comment HTML as plaintext.

    Converts all HTML tags and entities within 4chan comments
    into human-readable text equivalents.
    """
    body = _parser.unescape(body)
    body = re.sub(r'<a [^>]+>(.+?)</a>', r'\1', body)
    body = body.replace('<br>', '\n')
    body = re.sub(r'<.+?>', '', body)
    return body
