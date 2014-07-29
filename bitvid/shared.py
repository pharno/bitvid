__author__ = 'pharno'

import base64
from uuid import uuid4
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, current_app
from functools import wraps

from errors import LoginRequiredException
db = SQLAlchemy()


def generate_token():
    return str(uuid4())


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.session.user is None:
            raise LoginRequiredException()
        return f(*args, **kwargs)
    return decorated_function


def videofile_original_location(token, extention):
    return current_app.config[
        "VIDEO_STORE_PATH"] + current_app.config["VIDEO_ORIGINALS_PATH"] + token + "." + extention


def videofile_converted_location(token, height, extention):
    return current_app.config["VIDEO_STORE_PATH"] + current_app.config[
        "VIDEO_CONVERTED_PATH"] + token + "_" + str(height) + "." + extention


def videofile_webserver_path(token, height, extention):
    return "/videos/" + token + "_" + str(height) + "." + extention
