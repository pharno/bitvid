from flask import Flask, jsonify, request_finished, request
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from shared import db
import os
import traceback
from errors import errors

from baseapp import app


def make_json_error(ex):
    exceptionname = ex.__class__.__name__
    print exceptionname
    traceback.print_exc()
    if exceptionname in errors.keys():
        errordata = errors[exceptionname]
    else:
        errordata = errors["Exception"]

    if "message" in errordata.keys():
        response = jsonify(message=str(errordata["message"]))

    if "status" in errordata.keys():
        response.status_code = errordata["status"]

    return response


def init_db():
    with app.app_context():
        db.create_all()


@request_finished.connect_via(app)
def save_session(*args, **kwargs):
    request.session.save()


db.app = app
db.init_app(app)


from flask.ext import restful


class BitVidRestful(restful.Api):

    def handle_error(self, ex):
        return make_json_error(ex)


api = BitVidRestful(app, catch_all_404s=True)

from modules import userResource
userResource.register(api)

from modules import authResource
authResource.register(api)

from modules import videoResource
videoResource.register(api)

if __name__ == '__main__':
    app.run()
