
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from flask import request
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

from bitvid.shared import db, generate_token, login_required

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(4096))
    token = db.Column(db.String(128))

    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref("videos"))


    marshal_fields_create = {
        "token": fields.String
    }

    marshal_fields_get = {
        "id" : fields.Integer,
        "title" : fields.String,
        "description": fields.String
    }

    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.user = user
        self.token = generate_token()


    def __repr__(self):
        return '<video %r>' % self.title

class VideoResource(restful.Resource):
    @marshal_with(Video.marshal_fields_create)
    @login_required
    def post(self):
        # return the temporary video id which is used by the rest client to upload the video file
        # as it is not possible to upload raw json and a file at the same time

        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('description', required=False, type=str)
        args = parser.parse_args()

        newvideo = Video(args["title"],args["description"],request.session.user)
        db.session.add(newvideo)
        db.session.commit()

        print request.session.user.videos

        print newvideo.__dict__
        return newvideo


def register(api):
    api.add_resource(VideoResource, '/video/')
