#!/usr/bin/env python
# -*- coding: utf-8 -*-
URL = {
    'api': 'a.4cdn.org',
    'boards': 'boards.4chan.org',
    'images': 'i.4cdn.org',
    'thumbs': 't.4cdn.org',
    'template': {
        'board': '{name}/%s.json',
        'thread': '{name}/thread/%s.json'
    }
}

BOARDS = 'https://%s/boards.json' % URL['api']
CATALOG = 'catalog'
ALL_THREADS = 'threads'
