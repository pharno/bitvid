from bitvid.shared import db
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy import ForeignKey

from flask.ext.restful import fields
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))
    #sessions = relationship("Session")

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
        if len(password) < 8:
            raise ValueError("password to short (minimal length: 8)")
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email

    @validates("email")
    def validate_email(self,key,value):
        if len(value) > 8:
            return value
        else:
            raise ValueError("username to short (minimal length: 8)")
