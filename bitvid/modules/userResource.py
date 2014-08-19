__author__ = 'pharno'

from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from sqlalchemy.orm import relationship, backref

from bitvid.shared import db
from bitvid.errors import UserExistsException

from bitvid.models import User


class UserResource(restful.Resource):

    @marshal_with(User.marshal_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        userexists = User.query.filter_by(email=args["email"]).first()
        if userexists is not None:
            raise UserExistsException()

        user = User(args["email"], args["password"])
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()

        if not user:
            raise UserNotFoundException()

        if not user.check_password(args["password"]):
            raise IncorrectCredentialsException()

        db.session.delete(user)
        db.session.commit()

def register(api):
    api.add_resource(UserResource, '/user/')
