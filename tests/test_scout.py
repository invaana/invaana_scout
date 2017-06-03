from invaana_scout.scout import ScoutThis


def test_scout():
    scout = ScoutThis(kw="Ravi RT Merugu", max_pages=1)
    scout.run()
    result = scout.data
    assert type(result) is dict
    assert "results" in result
    assert "related_keywords" in result
    assert "search_kw" in result
    assert "search_kw_generated" in result