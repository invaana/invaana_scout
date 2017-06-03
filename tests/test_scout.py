from invaana_scout.scout import ScoutThis
import pytest


def test_scout():
    scout = ScoutThis(kw="Ravi RT Merugu", max_pages=1)
    scout.run()
    result = scout.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    assert "search_kw" in result
    assert "search_kw_generated" in result


def test_scout_browser():
    
    scout = ScoutThis(kw="Ravi RT Merugu", max_pages=1, browser="notbinga")
    
    with pytest.raises(NotImplementedError) as excinfo:
        scout.run()
    assert "Only bing search is implemented at this moment" in str(excinfo)
    
    
def test_keyword_generation():
    scout = ScoutThis(kw="Django", suffixes=['tutorials',], prefixes=['programming with',])
    assert scout.generated_keywords == ['programming with Django', 'Django tutorials' ]