__author__ = 'pharno'


from flask.sessions import SessionInterface, SessionMixin
from flask.ext.restful import reqparse, fields
from werkzeug.contrib.sessions import SessionStore


from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

import json

from shared import db
from uuid import uuid4

class Session(db.Model,SessionMixin):
	id = db.Column(db.Integer, primary_key=True)
	token = db.Column(db.String(128))
	_data = db.Column(db.String(16384))

	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	user = relationship("User",backref=backref("sessions"))

	marshal_fields = {
		"token": fields.String
	}

	def __init__(self, user):
		self.token = self._generate_token()
		self.user = user
		self.data = {}

	def _generate_token(self):
		return str(uuid4())

	@property
	def data(self):
		return json.loads(self._data)

	@data.setter
	def data(self,data):
		self._data = json.dumps(data)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def __getitem__(self,key):
		print "session.__getitem__({})".format(key)
		return self.data[key]

	def __setitem__(self,key,value):
		print "session.__setitem__({},{})".format(key,value)
		newdata = self.data.copy()
		newdata[key] = value

		self.data = newdata
		self.modified = True
		self.should_save = True

		print repr(self._data)

	def __delitem__(self,key):
		print "session.__delitem__({})".format(key)
		del self.data[key]

	def __repr__(self):
		return "<Session {token} for user {user}>".format(token=self.token,user=self.user)



class DBSessionInterface(SessionInterface):
	def open_session(self, app, request):
		parser = reqparse.RequestParser()
		parser.add_argument('token',type=str)

		params = parser.parse_args()


		if params["token"]:
			sqlsess = Session.query.filter_by(token=params["token"]).first()
			print "loading", sqlsess
			request.session = sqlsess

		if request.session is None: # if no token was sent or the session not found
			request.session = Session(user=None)

		print request.session

	def save_session(self, app, session, response):
		print "saaaaaving", session