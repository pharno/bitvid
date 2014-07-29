from flask import Flask
from session import DBSessionInterface
import os

app = Flask(__name__)
app.session_interface = DBSessionInterface()

curr_env = os.environ.get("BITVID_ENV", "Dev")
app.config.from_object("bitvid.config.{env}Config".format(env=curr_env))
app.environment = curr_env
