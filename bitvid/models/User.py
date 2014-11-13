from bitvid.shared import db
from bitvid.models.Mixins import Datemixin

from sqlalchemy.orm import validates
from flask.ext.restful import fields
from werkzeug.security import generate_password_hash, check_password_hash
from email.utils import parseaddr

class User(db.Model, Datemixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))
    #sessions = relationship("Session")

    marshal_fields = {
        "name": fields.String,
        "id": fields.Integer
    }

    def __init__(self, name, email, password):
        self.name = name
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
        return '<User %r>' % self.name

    @validates("name")
    def validate_name(self,key,value):
        if len(value) >= 3:
            return value
        else:
            raise ValueError("username to short (minimal length: 3)")

    @validates("email")
    def validate_email(self,key,value):
        print "validating email:", value
        if len(value) >= 3:
            return value
        else:
            raise ValueError("email to short (minimal length: 3)")

        parsed = parseaddr(value)
        newvalue = parsed[1]
        if newvalue:
            return newvalue

        raise ValueError("invalid email")