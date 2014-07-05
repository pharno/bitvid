__author__ = 'pharno'

from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from flask import request

from bitvid.shared import db
from bitvid.errors import UserExistsException

from bitvid.session import Session


class AuthResource(restful.Resource):
	@marshal_with(Session.marshal_fields)
	def post(self):
		request.session["loggedIn"] = True
		
		return request.session

class CounterResource(restful.Resource):
	# counter for testing purposes
	def post(self):
		try:
			request.session["counter"] += 1
		except KeyError:
			request.session["counter"] = 1
		return request.session["counter"]

	get = post

def register(api):
	api.add_resource(AuthResource, '/auth/')
	api.add_resource(CounterResource, '/counter/')
