#!/usr/bin/env python
# -*- coding: utf-8 -*-
URL = {
    'api': 'a.4cdn.org',          # API subdomain
    'boards': 'boards.4chan.org', # HTML subdomain
    'images': 'i.4cdn.org',       # image host
    'thumbs': 't.4cdn.org',       # thumbs host
    'template': {
        'board': '{name}/%s.json',
        'thread': '{name}/thread/%s.json'
    },
    'all_threads': 'threads',             # json entry for threads
    'catalog_dir': 'catalog',             # catalog directory 
    'boards_list': 'https://a.4cdn.org/boards.json'
}