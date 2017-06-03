from mongoengine import StringField, ListField, URLField, Document, ReferenceField, DateTimeField
from datetime import datetime


class SearchResultLink(Document):
    title = StringField()
    link = URLField()
    created_at = DateTimeField(default=datetime.now())
    
    meta = {
        'index_background': True,
        'index_drop_dups': True,
        'indexes': [
            'title',
        ],
    }


class SearchEntry(Document):
    keyword = StringField(required=True, unique=True)
    browser = StringField(choices=(
        ('bing', 'Bing'),
    ))
    results = ListField(ReferenceField(SearchResultLink))
    similar_keywords = ListField(StringField())
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField()
    meta = {
        'index_background': True,
        'index_drop_dups': True,
        'indexes': [
            'keyword',
        ]
    }