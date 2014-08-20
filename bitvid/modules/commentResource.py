__author__ = 'pharno'

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with

from bitvid.shared import login_required, db
from bitvid.models import Comment, Video
from bitvid.errors import NotFound
from bitvid.lib import Rest


class CommentCollectionResource(restful.Resource):

    @marshal_with(Comment.marshal_fields)
    @login_required
    def post(self, token):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('content', required=True, type=str)
        args = parser.parse_args()

        video = Video.query.filter_by(token=token).first()

        comment = Comment(
            args["title"],
            args["content"],
            request.session.user,
            video)
        db.session.add(comment)
        db.session.commit()
        return comment

    @marshal_with(
        {"comments": fields.List(fields.Nested(Comment.marshal_fields_get))})
    def get(self, token):
        video = Video.query.filter_by(token=token).first()
        return {"comments": video.comments}


class CommentResource(restful.Resource):

    @marshal_with(Comment.marshal_fields_get)
    def get(self, token):
        comment = Comment.query.filter_by(token=token).first()
        if not comment:
            raise NotFound()

        else:
            return comment

    @marshal_with(Comment.marshal_fields)
    @login_required
    def delete(self, token):
        comment = Comment.query.filter_by(token=token).first()
        db.session.delete(comment)
        db.session.commit()
        return comment

    @marshal_with(Comment.marshal_fields)
    @login_required
    def put(self, token):
        changedComment = Rest.updateModelFromRequest(
            Comment, {"token": token}, "title", "content")
        db.session.add(changedComment)
        db.session.commit()
        return changedComment


def register(api):
    api.add_resource(
        CommentCollectionResource, '/video/<string:token>/comments')
    api.add_resource(CommentResource, '/comment/<string:token>')
