from flask_login import UserMixin

from . import db


class ShortLink(db.Document):
    slug = db.StringField(max_length=30)
    original_url = db.URLField(max_length=500)
    user_id = db.StringField()
    access_counter = db.IntField(default=0)

    @property
    def created(self):
        return self.id.generation_time


class User(UserMixin, db.Document):
    username = db.StringField(max_length=30)
    email = db.EmailField(max_length=50)
    social_id = db.StringField(max_length=100)