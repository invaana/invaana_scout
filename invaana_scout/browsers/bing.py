from .base import BrowserBase


class BrowseBing(BrowserBase):
    """
    Does the browsing tasks on bing.com
    
    Usage:
        from invaana_scout.browsers.bing import BrowseBing
        bing = BrowseBing(kw="invaana", max_page=3)
        bing.search()
        bing.data # returns the data
    
    """
    _BASE_URL = 'https://www.bing.com'
    _SEARCH_QS = '/search?q='
    _SEARCH_MAIN_CSS_SELECTOR =  '.b_algo h2 a'
    _SEARCH_KEYWORDS_CSS_SELECTOR = '.b_rs a'
    _SEARCH_NEXT_QS = '&first='
    _SEARCH_NEXT_CSS_SELECTOR = 'a.sb_pagN'
    
    def __init__(self, kw=None, max_page=3):
        super(BrowseBing, self).__init__(kw=kw, max_page=max_page)