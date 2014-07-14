from bitvid.shared import db
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
