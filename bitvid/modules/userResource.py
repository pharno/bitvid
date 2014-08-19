__author__ = 'pharno'

from flask.ext import restful
from flask.ext.restful import reqparse, marshal_with

from bitvid.errors import UserExistsException, UserNotFoundException, \
    IncorrectCredentialsException
from bitvid.shared import db

from bitvid.models import User


class UserResource(restful.Resource):

    def _getAuthorizedUser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()

        if not user:
            raise UserNotFoundException()

        if not user.check_password(args["password"]):
            raise IncorrectCredentialsException()

        return user

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
        user = self._getAuthorizedUser()

        db.session.delete(user)
        db.session.commit()

    @marshal_with(User.marshal_fields)
    def put(self):
        user = self._getAuthorizedUser()

        parser = reqparse.RequestParser()
        parser.add_argument('newpassword', required=True, type=str)
        args = parser.parse_args()

        user.password = args["newpassword"]
        db.session.add(user)
        db.session.commit()

        return user


def register(api):
    api.add_resource(UserResource, '/user/')
