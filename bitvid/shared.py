__author__ = 'pharno'

import base64
import os
import errno

from uuid import uuid4
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, current_app
from functools import wraps

from errors import LoginRequiredException
db = SQLAlchemy()

from raven.contrib.flask import Sentry
sentry = Sentry()


def get_es():
    from pyelasticsearch import ElasticSearch
    elasticsearch = ElasticSearch(current_app.config["ELASTICSEARCH_URL"])
    return elasticsearch


def get_es_index():
    return current_app.config["ELASTICSEARCH_INDEX"]


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
    return current_app.config["VIDEO_STORE_PATH"] + \
        current_app.config["VIDEO_ORIGINALS_PATH"] + token + "." + extention


def videofile_converted_location(token, height, extention):
    return current_app.config["VIDEO_STORE_PATH"] + current_app.config[
        "VIDEO_CONVERTED_PATH"] + token + "_" + str(height) + "." + extention


def videofile_webserver_path(token, height, extention):
    return "/videos/" + token + "_" + str(height) + "." + extention


def thumbnail_location(token):
    return current_app.config["THUMBNAIL_STORE_PATH"] + token + ".jpg"


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
