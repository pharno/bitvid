from bitvid.shared import db, generate_token, login_required, videofile_original_location, get_es, get_es_index

from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy import ForeignKey
from sqlalchemy import event


from flask.ext.restful import fields


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(4096))
    token = db.Column(db.String(128))
    originalmime = db.Column(db.String(8))

    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref("videos"))

    marshal_fields_create = {
        "token": fields.String
    }

    marshal_fields = {
        "token": fields.String,
        "title": fields.String,
        "description": fields.String
    }

    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.user = user
        self.token = generate_token()

    def __repr__(self):
        return '<video %r>' % self.title

    @validates("title")
    def validate_title(self, key, value):
        if len(value) >= 8:
            return value
        else:
            raise ValueError("title to short (minimum length: 8)")

    @validates("description")
    def validate_description(self, key, value):
        if len(value) >= 8:
            return value
        else:
            raise ValueError("description to short (minimum length: 8)")


def index_video(mapper, connection, target):
    toindex = {
        "id": target.id,
        "title": target.title,
        "description": target.description,
        "mime": target.originalmime,
        "user_id": target.user_id,
        "user_name": target.user.email,
        "token": target.token
    }

    get_es().index(get_es_index(), target.__class__.__name__, toindex, id=target.token)


event.listen(Video, 'after_insert', index_video)
event.listen(Video, 'after_update', index_video)


class ConvertedVideo(db.Model):
    marshal_fields = {
        "height": fields.Integer,
        "codec": fields.String
    }

    def __init__(self, video, height, codec):
        self.original = video
        self.height = height
        self.codec = codec

    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer, ForeignKey("video.id"))
    original = relationship("Video", backref=backref("convertedVideos"))
    height = db.Column(db.Integer)
    codec = db.Column(db.String(8))
