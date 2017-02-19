import datetime

from . import db


class ShortLink(db.Document):
    slug = db.StringField(max_length=30)
    destination_url = db.URLField(max_length=500)
    created = db.DateTimeField(default=datetime.datetime.now)
