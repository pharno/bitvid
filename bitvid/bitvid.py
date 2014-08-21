from flask import request_finished, request

from shared import db
from baseapp import app
from lib.BitVidRestful import BitVidRestful


def init_db():
    with app.app_context():
        db.create_all()


def destroy_db():
    with app.app_context():
        db.drop_all()


@request_finished.connect_via(app)
def save_session(*args, **kwargs):
    request.session.save()


db.app = app
db.init_app(app)


api = BitVidRestful(app, catch_all_404s=True)

from modules import userResource
userResource.register(api)

from modules import authResource
authResource.register(api)

from modules import videoResource
videoResource.register(api)

from modules import commentResource
commentResource.register(api)


if __name__ == '__main__':
    app.run()
