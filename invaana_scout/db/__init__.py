from mongoengine import connect
from .mongo import SearchEntry, SearchResultLink


connect('invaana_scout')