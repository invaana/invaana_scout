import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCOUT_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCOUT_PATH)


from invaana_scout.browsers.bing import BrowseBing, BrowserBase
bing = BrowseBing(kw="invaana")
print bing.search()