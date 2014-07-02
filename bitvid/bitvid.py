from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from shared import db
import os

from errors import errors

app = Flask(__name__)

def make_json_error(ex):
	response = jsonify(message=str(ex))
	exceptionname = ex.__class__.__name__

	if exceptionname in errors.keys():
		errordata = errors[exceptionname]
		if "message" in errordata.keys():
			response = jsonify(message=str(errordata["message"]))

		if "status" in errordata.keys():
			response.status_code = errordata["status"]

	else:
		response.status_code = (ex.code
								if isinstance(ex, HTTPException)
								else 500)
	return response

db.app = app
db.init_app(app)

curr_env = os.environ.get("BITVID_ENV","Dev")
app.config.from_object("bitvid.config.{env}Config".format(env=curr_env))

from flask.ext import restful

class BitVidRestful(restful.Api):
	def handle_error(self,ex):
		return make_json_error(ex)

api = BitVidRestful(app)

from modules import auth
auth.register(api)

def init_db():
	with app.app_context():
		db.create_all()

if __name__ == '__main__':
	app.run()
