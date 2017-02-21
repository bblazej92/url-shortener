from flask_login import UserMixin

from . import db


class ShortLink(db.Document):
    slug = db.StringField(max_length=30)
    original_url = db.URLField(max_length=500)
    created = db.DateTimeField()
    user_id = db.StringField()


class User(UserMixin, db.Document):
    username = db.StringField(max_length=30)
    email = db.EmailField(max_length=50)
    social_id = db.StringField(max_length=100)
