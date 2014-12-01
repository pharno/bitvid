__author__ = 'pharno'

from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from flask import request

from bitvid.shared import db
from bitvid.errors import UserExistsException, UserNotFoundException, IncorrectCredentialsException
from bitvid.modules.userResource import User
from bitvid.session import Session


class AuthResource(restful.Resource):

    @marshal_with(Session.marshal_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()

        user = User.query.filter_by(name=args["name"]).first()

        if not user:
            raise UserNotFoundException()

        if not user.check_password(args["password"]):
            raise IncorrectCredentialsException()

        request.session["loggedIn"] = True
        request.session.user = user

        return request.session


class CounterResource(restful.Resource):
    # counter for testing purposes

    def post(self):
        print request.session.user.sessions
        try:
            request.session["counter"] += 1
        except KeyError:
            request.session["counter"] = 1
        return request.session["counter"]

    get = post


def register(api):
    api.add_resource(AuthResource, '/auth')
    api.add_resource(CounterResource, '/counter')
