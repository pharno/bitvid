__author__ = 'pharno'

import base64
from uuid import uuid4
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_token():
    return str(uuid4())