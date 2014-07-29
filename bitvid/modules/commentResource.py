__author__ = 'pharno'

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from sqlalchemy.orm import relationship, backref

from bitvid.shared import login_required, db
from bitvid.models import Comment
from bitvid.errors import NotFound


class CommentCollectionResource(restful.Resource):

    @marshal_with(Comment.marshal_fields)
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('content', required=True, type=str)
        args = parser.parse_args()

        comment = Comment(
            args["title"],
            args["content"],
            request.session.user,
            None)
        db.session.add(comment)
        db.session.commit()
        return comment


class CommentResource(restful.Resource):

    @marshal_with(Comment.marshal_fields_get)
    def get(self, token):
        comment = Comment.query.filter_by(token=token).first()
        if not comment:
            raise NotFound()

        else:
            return comment


def register(api):
    api.add_resource(CommentCollectionResource, '/comment/')
    api.add_resource(CommentResource, '/comment/<string:token>')
