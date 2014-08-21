import traceback
from flask import jsonify
from flask.ext import restful

from flask.ext.restful import marshal_with


from bitvid.errors import errors, NotFound
from bitvid.lib import Rest
from bitvid.models import Comment
from bitvid.shared import login_required, db


def make_json_error(ex):
    exceptionname = ex.__class__.__name__

    # traceback.print_exc()
    if exceptionname in errors.keys():
        errordata = errors[exceptionname]
    else:
        errordata = errors["Exception"]
        traceback.print_exc()

    if "message" in errordata.keys():
        response = jsonify(message=str(errordata["message"]))

    if "status" in errordata.keys():
        response.status_code = errordata["status"]

    return response


class BitVidRestful(restful.Api):
    def handle_error(self, ex):
        return make_json_error(ex)


class BitVidRestResource(restful.Resource):
    updatefields = []
    baseModel = None

    def _get(self, **kwargs):
        model = self.baseModel.query.filter_by(**kwargs).first()
        if not model:
            raise NotFound()

        else:
            return model

    def _delete(self, **kwargs):
        deletedmodel = self.baseModel.query.filter_by(**kwargs).first()
        db.session.delete(deletedmodel)
        db.session.commit()
        return deletedmodel

    def _put(self, **kwargs):
        changedmodel = Rest.updateModelFromRequest(
            self.baseModel, kwargs, *self.updatefields)
        db.session.add(changedmodel)
        db.session.commit()
        return changedmodel
