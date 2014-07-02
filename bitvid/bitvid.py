from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from shared import db

import os

app = Flask(__name__)

def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response

for code in default_exceptions.iterkeys():
    app.error_handler_spec[None][code] = make_json_error

db.app = app
db.init_app(app)

curr_env = os.environ.get("BITVID_ENV","Dev")
app.config.from_object("bitvid.config.{env}Config".format(env=curr_env))

from flask.ext import restful
api = restful.Api(app)

from modules import auth
auth.register(api)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run()
