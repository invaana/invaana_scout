from invaana_scout.browsers import BrowseBing


def test_browse_with_bing():
    bing = BrowseBing(kw="Ravi RT Merugu", max_page=1)
    bing.search()
    result = bing.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result