__author__ = 'pharno'

from bitvid.shared import db
from flask.ext import restful


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def set_password(self,password):
        pass

    def __repr__(self):
        return '<User %r>' % self.username


class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


def register(api):
    api.add_resource(HelloWorld, '/')
