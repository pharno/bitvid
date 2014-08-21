__author__ = 'pharno'

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with

from bitvid.shared import login_required, db
from bitvid.models import Comment, Video
from bitvid.lib import BitVidRestful


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


class CommentResource(BitVidRestful.BitVidRestResource):
    updatefields = ["title", "content"]
    baseModel = Comment

    @marshal_with(Comment.marshal_fields_get)
    def get(self, token):
        return self._get(token=token)

    @marshal_with(Comment.marshal_fields)
    @login_required
    def delete(self, token):
        return self._delete(token=token)

    @marshal_with(baseModel.marshal_fields)
    @login_required
    def put(self, token):
        return self._put(token=token)


def register(api):
    api.add_resource(
        CommentCollectionResource, '/video/<string:token>/comments')
    api.add_resource(CommentResource, '/comment/<string:token>')
