from flask import Flask
from shared import db

import os

app = Flask(__name__)

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
