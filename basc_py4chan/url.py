#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 4chan URL generator. Inherit and override this for derivative classes  (e.g. 420chan API, 8chan/vichan API)
class Url():
    # default value for board in case user wants to query board list
    def __init__(self, board, https=False):
        self._board = board
        self._protocol = 'https://' if https else 'http://'
        
        # 4chan API URL Subdomains
        DOMAIN = {
            'api': self._protocol + 'a.4cdn.org',   # API subdomain
            'boards': self._protocol + 'boards.4chan.org', # HTML subdomain
            'file': self._protocol + 'i.4cdn.org',  # file (image) host
            'thumbs': self._protocol + 'i.4cdn.org',# thumbs host
            'static': self._protocol + 's.4cdn.org' # static host
        }
        
        # 4chan API URL Templates
        TEMPLATE = {
            'api': {  # URL structure templates
                'board': DOMAIN['api'] + '/{board}/{page}.json',
                'thread': DOMAIN['api'] + '/{board}/thread/{thread_id}.json'
            },
            'http': { # Standard HTTP viewing URLs
                'board': DOMAIN['boards'] + '/{board}/{page}.json',
                'thread': DOMAIN['boards'] + '/{board}/thread/{thread_id}'
            },
            'data': {
                'file': DOMAIN['file'] + '/{board}/{tim}{ext}',
                'thumbs': DOMAIN['thumbs'] + '/{board}/{tim}s.jpg',
                'static': DOMAIN['static'] + '/image/{item}'
            }
        }
        
        # 4chan API Listings
        LISTING = {
            'board_list': DOMAIN['api'] + '/boards.json',
            'thread_list': DOMAIN['api'] + '/{board}/threads.json',
            'archived_thread_list': DOMAIN['api'] + '/{board}/archive.json',
            'catalog': DOMAIN['api'] + '/{board}/catalog.json'
        }
        
        # combine all dictionaries into self.URL dictionary
        self.URL = TEMPLATE
        self.URL.update({'domain': DOMAIN})
        self.URL.update({'listing': LISTING})

    # generate boards listing URL
    def board_list(self):
        return self.URL['listing']['board_list']

    # generate board page URL
    def page_url(self, page):
        return self.URL['api']['board'].format(
            board=self._board,
            page=page
            )

    # generate catalog URL
    def catalog(self):
        return self.URL['listing']['catalog'].format(
            board=self._board
            )

    # generate threads listing URL
    def thread_list(self):
        return self.URL['listing']['thread_list'].format(
            board=self._board
            )

#    # generate archived threads list URL (disabled for compatibility)
#    def archived_thread_list(self):
#        return self.URL['listing']['archived_thread_list'].format(
#            board=self._board
#            )

    # generate API thread URL
    def thread_api_url(self, thread_id):
        return self.URL['api']['thread'].format(
            board=self._board,
            thread_id=thread_id
            )

    # generate HTTP thread URL
    def thread_url(self, thread_id):
        return self.URL['http']['thread'].format(
            board=self._board,
            thread_id=thread_id
            )

    # generate file URL
    def file_url(self, tim, ext):
        return self.URL['data']['file'].format(
            board=self._board,
            tim=tim,
            ext=ext
            )

    # generate thumb URL
    def thumb_url(self, tim):
        return self.URL['data']['thumbs'].format(
            board=self._board,
            tim=tim
            )

    # return entire URL dictionary
    @property
    def site_urls(self):
        return self.URL

"""
# 4chan Static Data (Unique to 4chan, needs implementation)
STATIC = {
    'flags': DOMAIN['static'] + '/image/country/{country}.gif',
    'pol_flags': DOMAIN['static'] + '/image/country/troll/{country}.gif',
    'spoiler': { # all known custom spoiler images, just fyi
        'default': DOMAIN['static'] + '/image/spoiler.png',
        'a': DOMAIN['static'] + '/image/spoiler-a.png',
        'co': DOMAIN['static'] + '/image/spoiler-co.png',
        'mlp': DOMAIN['static'] + '/image/spoiler-mlp.png',
        'tg': DOMAIN['static'] + '/image/spoiler-tg.png',
        'tg-alt': DOMAIN['static'] + '/image/spoiler-tg2.png',
        'v': DOMAIN['static'] + '/image/spoiler-v.png',
        'vp': DOMAIN['static'] + '/image/spoiler-vp.png',
        'vr': DOMAIN['static'] + '/image/spoiler-vr.png'
    }
}
"""
