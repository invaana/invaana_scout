import contextlib
import selenium.webdriver as webdriver
import lxml, os, subprocess
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
    _CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'

    
    _AVAILABLE_SCRAPE_METHODS = ['requests', 'selenium']
    _DEFAULT_SCRAPE_METHOD = "selenium"

    _BASE_URL = None
    _SEARCH_QS = None
    _SEARCH_TERM = None
    _SEARCH_URL = None

    _HTML_DATA = None
    _SOUPED_HTML_DATA = None

    _RESULTS_MAIN = []
    _RESULTS_KEYWORDS = []

    _SEARCH_MAIN_CSS_SELECTOR = None
    _SEARCH_KEYWORDS_CSS_SELECTOR = None
    _SEARCH_NEXT_CSS_SELECTOR = None
    
    _NEXT_PAGE_URL = None
    
    _ITER = 0
    _ITER_MAX = 10
        
    def __init__(self, kw=None, max_page=None):
        """
        Make some quick calculations to proceed with the run
        """
        self._SEARCH_TERM = kw
        if max_page:
            self._ITER_MAX = max_page

            
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
        # options.add_argument("--headless")
        # with contextlib.closing(webdriver.Chrome(chrome_options=options)) as driver:
        with contextlib.closing(webdriver.Chrome(self._CHROME_DRIVER_PATH)) as driver:
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
        if self._ITER == 0:
            self._SEARCH_URL = self._BASE_URL + self._SEARCH_QS + self._SEARCH_TERM
        self.dry_run()
        self._test_config()
        self._HTML_DATA = self.get_html()
        self._SOUPED_HTML_DATA = self._soup_data()
        self._RESULTS_MAIN += self.get_search_results()
        self._RESULTS_KEYWORDS += self.get_related_keywords()
        self._NEXT_PAGE_URL = self._get_next_page()
        
        if self._NEXT_PAGE_URL and self._ITER < self._ITER_MAX:
            self._ITER += 1
            self.search()
        
    
    @property
    def data(self):
        return {
            'results': self._RESULTS_MAIN,
            'results_count': len(self._RESULTS_MAIN),
            'related_keywords': self._RESULTS_KEYWORDS,
            'related_keywords_count': len(self._RESULTS_KEYWORDS),
            'next_url': self._NEXT_PAGE_URL
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
    
    def _get_next_page(self):
        """
        :return:
        """
        el = self._SOUPED_HTML_DATA.cssselect(self._SEARCH_NEXT_CSS_SELECTOR)
        if len(el) >= 1:
            el = el[0]
            return self._BASE_URL + el.get('href').strip()
        else:
            return None
        
    def get_search_results(self):
        return self._scrape_css_selector(self._SEARCH_MAIN_CSS_SELECTOR)
    
    def get_related_keywords(self):
        return self._scrape_css_selector(self._SEARCH_KEYWORDS_CSS_SELECTOR)

