from invaana_scout.db.utils import get_or_create
from invaana_scout.db.mongo import SearchEntry
import string, random


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def test_get_or_create():
    random_string = id_generator()
    created, entry = get_or_create(SearchEntry, keyword=random_string) # this will test create part
    assert created == False
    
    created, entry = get_or_create(SearchEntry, keyword=random_string) # this will test get part
    assert created == True
