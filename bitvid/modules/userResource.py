__author__ = 'pharno'

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, marshal_with

from bitvid.errors import UserExistsException, UserNotFoundException, \
    IncorrectCredentialsException
from bitvid.shared import db

from bitvid.models import User


class UserCollectionResource(restful.Resource):

    def _getAuthorizedUser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        user = User.query.filter_by(name=args["name"]).first()

        if not user:
            raise UserNotFoundException()

        if not user.check_password(args["password"]):
            raise IncorrectCredentialsException()

        return user

    @marshal_with(User.marshal_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        userexists = User.query.filter_by(name=args["name"]).first()
        if userexists is not None:
            raise UserExistsException()

        userexists = User.query.filter_by(email=args["email"]).first()
        if userexists is not None:
            raise UserExistsException()

        user = User(args["name"], args["email"], args["password"])
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


class UserResource(restful.Resource):

    @marshal_with(User.marshal_fields)
    def get(self, user):
        if user.lower() == "current":
            return request.session.user

        usermodel = User.query.filter_by(id=user).first()

        print usermodel
        return usermodel


def register(api):
    api.add_resource(UserCollectionResource, '/user/')
    api.add_resource(UserResource, '/user/<string:user>')
