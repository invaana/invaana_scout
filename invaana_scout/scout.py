from invaana_scout.db import SearchResultLink, SearchEntry
from browsers import BrowseBing
from invaana_scout.db.utils import get_or_create


class ScoutThis(object):
    """
    This will run a browser search and saves the data to the MongoDB
    
    USAGE:
        from invaana_scout.scout import ScoutThis

        scout = ScoutThis(kw="Scientific Innovations")
        scout.run()
    
    """
    
    def __init__(self, kw=None, browser='bing', max_pages=3, save=True):
        self._KEYWORD = kw
        self._BROWSER = browser
        self._MAX_PAGES = max_pages
        self._SAVE = save
            
    def save(self, data):
        """
        Saves this to DB (MongoDB) for now
        :param data:
        :return:
        """
        created, entry = get_or_create(SearchEntry, keyword=self._KEYWORD, browser=self._BROWSER)
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

    def run(self,):
        if self._BROWSER == 'bing':
            browser = BrowseBing(kw=self._KEYWORD, max_page=self._MAX_PAGES)
            browser.search()
            print "Gathered the data for keyword", self._KEYWORD
            if self._SAVE:
                print "Now saving the data to DB"
                self.save(browser.data)
        else:
            NotImplementedError("Only bing search is implemented at this moment, contact author for more info")