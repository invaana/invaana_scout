from db import SearchResultLink, SearchEntry
from browsers import BrowseBing
from db.utils import get_or_create
import selenium.webdriver as webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

class ScoutThis(object):
    """
    This will run a browser search and saves the data to the MongoDB
    
    USAGE:
        from invaana_scout.scout import ScoutThis
        
        scout = ScoutThis(kw="MongoDB", generate_kws=True)
        scout.generated_keywords # ['learning MongoDB', 'Programming with MongoDB', 'MongoDB tutorials' ]
        scout.run() # this will gather data from all generated keywords and saves it to MongoDB
        
        # or
        
        scout = ScoutThis(kw="MongoDB")
        scout.run() # this will gather data and saves it to MongoDB
        

    
    """
 
    _SUFFIXES = [ 'tutorials', ]
    _PREFIXES = [ 'learning', 'Programming with' ]
    
    def __init__(self, kw=None, browser='bing', max_pages=3, save=True,
                 generate_kws=False,
                 prefixes=_PREFIXES,
                 suffixes=_SUFFIXES):
        self._KEYWORD = kw
        self._BROWSER = browser
        self._NOW_KEYWORD = kw
        self._MAX_PAGES = max_pages
        self._SAVE = save
        self._GENERATE_KWS = generate_kws
        self._GENERATED_KEYWORDS = []
        self._DATA = {
            'results': [],
            'results_count': 0,
            'related_keywords' : [],
            'related_keywords_count' : 0,
            'search_kw': '',
            'search_kw_generated': []
        
        }
        if prefixes: self._PREFIXES = prefixes
        if suffixes: self._SUFFIXES = suffixes
        
        self._init_browser_instance()
            
    def save(self, data):
        """
        Saves this to DB (MongoDB) for now
        :param data:
        :return:
        """
        created, entry = get_or_create(SearchEntry, keyword=self._NOW_KEYWORD)
        entry.update(browser=self._BROWSER)
        results_mongofied = []
        for result in data['results']:
            created, result_entry = get_or_create(SearchResultLink, title=result['text'], link=result['link'] )
            results_mongofied.append(result_entry)
            
        if len(results_mongofied) > 0:
            entry.update(add_to_set__results=list(set(results_mongofied)))

        related_keywords_mongofied = []
        for keyword in data['related_keywords']:
            related_keywords_mongofied.append(keyword['text'])

        if len(related_keywords_mongofied)>0:
            entry.update(add_to_set__similar_keywords=related_keywords_mongofied)

    @property
    def generated_keywords(self):
        if len(self._GENERATED_KEYWORDS) == 0:
            self._GENERATED_KEYWORDS = self._generate_keywords()
        return self._GENERATED_KEYWORDS
        
    @property
    def data(self):
        return self._DATA
    
    def _init_browser_instance(self):
        self._DRIVER = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME)
        
    def _generate_keywords(self):
        keywords = []
        for prefix in self._PREFIXES:
            keywords.append("%s %s" % (prefix, self._KEYWORD))
    
        for suffix in self._SUFFIXES:
            keywords.append("%s %s" % (self._KEYWORD, suffix))
        return keywords

    def _append_data(self, data):
        self._DATA['results'] += data['results']
        self._DATA['related_keywords'] += data['related_keywords']
        self._DATA['related_keywords_count'] += data['related_keywords_count']
        self._DATA['results_count'] += data['results_count']
        self._DATA['search_kw'] = self._KEYWORD
        self._DATA['search_kw_generated'] = self.generated_keywords
        
    def _run(self, kw):
        if self._BROWSER == 'bing':
            browser = BrowseBing(kw=kw, max_page=self._MAX_PAGES, driver=self._DRIVER)
            browser.search()
            print "Gathered the data for keyword", kw
            self._append_data(browser.data)
            if self._SAVE:
                print "Now saving the keyword [ %s ] data to DB" %kw
                self.save(browser.data)
        else:
            raise NotImplementedError("Only bing search is implemented at this moment, contact author for more info")
            
    def run(self):
        """
        Runs the data gathering jobs -
            **if self._GENERATE_KWS == True:** new keywords will be generated based on the prefixes, and suffixes is
            True, it will iterate through each keyword and gathers the information **else:** single keyword
            provided to the __init__() will be used and gathered data.
            
        :return:
        
        """
        if self._GENERATE_KWS:
            self._GENERATED_KEYWORDS = self.generated_keywords
            print "Generated %s keywords for [%s] " %(len(self._GENERATED_KEYWORDS), self._KEYWORD)
            for kw in self._GENERATED_KEYWORDS:
                self._NOW_KEYWORD = kw
                self._run(self._NOW_KEYWORD)
        else:
            self._run(self._NOW_KEYWORD)
            
    def stop(self):
        self._DRIVER.close()