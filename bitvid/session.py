__author__ = 'pharno'


from flask.sessions import SessionInterface, SessionMixin
from flask import request

from flask.ext.restful import reqparse, fields
from werkzeug.contrib.sessions import SessionStore


from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

import json
import arrow

from shared import db, generate_token
from uuid import uuid4


class Session(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128))
    _data = db.Column(db.String(16384))

    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref('sessions', order_by=id))

    marshal_fields = {
        "token": fields.String
    }

    def __init__(self, user):
        self.token = generate_token()
        self.user = user
        self.data = {}
        self["firstLoginIP"] = request.remote_addr
        self["createdAt"] = str(arrow.utcnow())

    @property
    def data(self):
        return json.loads(self._data)

    @data.setter
    def data(self, data):
        self._data = json.dumps(data)

    @property
    def createdAt(self):
        return arrow.get(self.data["createdAt"])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        newdata = self.data.copy()
        newdata[key] = value

        self.data = newdata
        self.modified = True
        self.should_save = True

    def __delitem__(self, key):
        del self.data[key]

    def __repr__(self):
        return "<Session {token} for user {user}>".format(
            token=self.token,
            user=self.user)


class DBSessionInterface(SessionInterface):

    def open_session(self, app, request):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location="headers")

        params = parser.parse_args()

        request.session = None
        if params["token"]:
            sqlsess = Session.query.filter_by(token=params["token"]).first()
            print "loading", sqlsess
            request.session = sqlsess

        # if no token was sent or the session not found
        if request.session is None:
            request.session = Session(user=None)
