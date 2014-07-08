__author__ = 'pharno'

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from sqlalchemy.orm import relationship, backref

from bitvid.shared import db
from bitvid.errors import UserExistsException

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))
    #sessions = relationship("Session", backref="user")

    marshal_fields = {
        "email": fields.String,
        "id": fields.Integer
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email


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


def register(api):
    api.add_resource(UserResource, '/user/')
