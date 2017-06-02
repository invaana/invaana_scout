import contextlib
import selenium.webdriver as webdriver
import lxml, os
import lxml.html
from . import exceptions
import logging

class BrowserBase(object):
    """
    Base class for making new browser classes like BingBrowser, GoogleBrowser, DuckDuckGoBrowser etc
    
    
    USAGE:
        _BASE_URL : https://www.bing.com # this should be changed for each Child class
        _PHANTOMJS_PATH : #phantomjs binary path
        _DEFAULT_METHOD : #default method used to scrape ? selenium or python requests
        
    """
    _AVAILABLE_SCRAPE_METHODS = ['requests', 'selenium']
    _DEFAULT_SCRAPE_METHOD = "selenium"
    _BASE_URL = None
    _SEARCH_QS = '/search?q='
    _SEARCH_URL = None
    _HTML_DATA = None
    _SOUPED_HTML_DATA = None
    _RESULTS_MAIN = []
    _RESULTS_KEYWORDS = []
    _SEARCH_MAIN_CSS_SELECTOR = None
    _SEARCH_KEYWORDS_CSS_SELECTOR = None
    _SEARCH_TERM = None
    
    def __init__(self, kw=None):
        """
        Make some quick calculations to proceed with the run
        """
        self._SEARCH_TERM = kw

            
    def _test_config(self):
        """
        this will check the inputs and executables being in place
        :return:
        """
        logging.debug('testing config')
    
    def _soup_data(self):
         return lxml.html.fromstring(self._HTML_DATA)
    
    def get_html_selenium(self):
        """
        https://stackoverflow.com/a/18102579/3448851
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        with contextlib.closing(webdriver.Chrome(chrome_options=options)) as driver:
            driver.get(url=self._SEARCH_URL)
            return driver.page_source
    
    def get_html_requests(self):
        pass
        
    def get_html(self, method=None):
        if method is None:
            method = self.get_current_method()
        if method == 'selenium':
            return self.get_html_selenium()
        elif method == 'requests':
            raise exceptions.BrowerScrapeMethodNotImplemented('Not implemented')
        
    def dry_run(self):
        """
        This will run a dry run with plain python requests, and check if requests is good enough,
        and if there is some issue, the driver will be switched to Selenium
        :return:
        """
        pass
    
    def get_current_method(self):
        """
        Returns the current Browser driver being used by this class (requests or selenium)
        :return:
        """
        return self._DEFAULT_SCRAPE_METHOD
    
    def shift_method(self):
        """
        swaps the current method to other method. If python requests is current method, it will shift to next one, which is
        selenium
        :return:
        """
        index = self._AVAILABLE_SCRAPE_METHODS.index(self._DEFAULT_SCRAPE_METHOD)
        self._DEFAULT_SCRAPE_METHOD = self._AVAILABLE_SCRAPE_METHODS[index+1]
    
    def search(self):
        """
         1. Perform a dry run
         2. shift _DEFAULT_SCRAPE_METHOD if needed
         3. get results
         """
        self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + self._SEARCH_TERM
        self.dry_run()
        self._test_config()
        self._HTML_DATA = self.get_html()
        self._SOUPED_HTML_DATA = self._soup_data()
        self._RESULTS_MAIN = self.get_search_results()
        self._RESULTS_KEYWORDS = self.get_related_keywords()
        return self.data
        
    @property
    def data(self):
        return {
            'results': self._RESULTS_MAIN,
            'results_count': len(self._RESULTS_MAIN),
            'related_keywords': self._RESULTS_KEYWORDS,
            'related_keywords_count': len(self._RESULTS_KEYWORDS)
        }

    def _scrape_css_selector(self, selector=None):
        results = self._SOUPED_HTML_DATA.cssselect(selector)
        data = []
        for result in results:
            datum = {
                'link': result.get('href').strip() if result.get('href') else None,
                'text': result.text_content().strip() if result.text_content() else None
            }
            data.append(datum)
        return data
        
    def get_search_results(self):
        return self._scrape_css_selector(self._SEARCH_MAIN_CSS_SELECTOR)
    
    def get_related_keywords(self):
        return self._scrape_css_selector(self._SEARCH_KEYWORDS_CSS_SELECTOR)

    def get_page(self, page_no=None):
        """
        Get the number of page result
        :return:
        """
        pass