from invaana_scout.db import SearchResultLink, SearchEntry
from invaana_scout.browsers import BrowseBing
from invaana_scout.db.utils import get_or_create


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
    
    def __init__(self, kw=None, browser='bing', max_pages=3, save=True, generate_kws=False):
        self._KEYWORD = kw
        self._BROWSER = browser
        self._NOW_KEYWORD = kw
        self._MAX_PAGES = max_pages
        self._SAVE = save
        self._GENERATE_KWS = generate_kws
        self._SUFFIXES = [
            'tutorials',
        ]
        self._PREFIXES = [
            'learning', 'Programming with'
        ]
        self._GENERATED_KEYWORDS = []
            
    def save(self, data):
        """
        Saves this to DB (MongoDB) for now
        :param data:
        :return:
        """
        created, entry = get_or_create(SearchEntry, keyword=self._NOW_KEYWORD, browser=self._BROWSER)
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
        return self._GENERATED_KEYWORDS
    
    def _generate_keywords(self):
        keywords = []
        for prefix in self._PREFIXES:
            keywords.append("%s %s" % (prefix, self._KEYWORD))
    
        for suffix in self._SUFFIXES:
            keywords.append("%s %s" % (self._KEYWORD, suffix))
        return keywords

    def _run(self, kw):
        if self._BROWSER == 'bing':
            browser = BrowseBing(kw=kw, max_page=self._MAX_PAGES)
            browser.search()
            print "Gathered the data for keyword", kw
            if self._SAVE:
                print "Now saving the keyword [ %s ] data to DB" %kw
                self.save(browser.data)
        else:
            NotImplementedError("Only bing search is implemented at this moment, contact author for more info")
            
    def run(self):
        """
        Runs the data gathering jobs -
            **if self._GENERATE_KWS == True:** new keywords will be generated based on the prefixes, and suffixes is
            True, it will iterate through each keyword and gathers the information **else:** single keyword
            provided to the __init__() will be used and gathered data.
            
        :return:
        
        """
        if self._GENERATE_KWS:
            self._GENERATED_KEYWORDS = self._generate_keywords()
            print "Generated %s keywords for [%s] " %(len(self._GENERATED_KEYWORDS), self._KEYWORD)
            for kw in self._GENERATED_KEYWORDS:
                self._NOW_KEYWORD = kw
                self._run(self._NOW_KEYWORD)
        else:
            self._run(self._NOW_KEYWORD)