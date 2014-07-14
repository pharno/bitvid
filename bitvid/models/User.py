from bitvid.shared import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

from flask.ext.restful import fields


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
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email
