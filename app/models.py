import datetime

from . import db


class ShortLink(db.Document):
     slug = db.StringField(max_length=8)
     destination_url = db.URLField(max_length=500)
     timestamp = db.DateTimeField(default=datetime.datetime.now)
