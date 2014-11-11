from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, validates
from flask.ext.restful import fields

from bitvid.shared import db, generate_token
from bitvid.models.Mixins import Datemixin


class AuthorField(fields.Raw):

    def format(self, user):
        return user.name


class Comment(db.Model, Datemixin):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.String(4096))
    token = db.Column(db.String(128))

    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref("comments"))

    video_id = db.Column(db.Integer, ForeignKey('video.id'))
    video = relationship("Video", backref=backref("comments"))

    marshal_fields = {
        "token": fields.String,
    }

    marshal_fields_get = {
        "token": fields.String,
        "title": fields.String,
        "content": fields.String,
        "author": AuthorField(attribute="user")
    }

    def __init__(self, title, content, user, video):
        self.title = title
        self.content = content
        self.user = user
        self.video = video
        self.token = generate_token()

    #@validates("title")
    def validate_title(self, key, value):
        if len(value) >= 8:
            return value
        else:
            raise ValueError("title to short (minimum length: 8)")

    @validates("content")
    def validate_content(self, key, value):
        if len(value) >= 8:
            return value
        else:
            raise ValueError("content to short (minimum length: 8)")
