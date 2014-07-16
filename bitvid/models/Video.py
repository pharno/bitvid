from bitvid.shared import db, generate_token, login_required, videofile_original_location

from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

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
        "id": fields.Integer,
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
