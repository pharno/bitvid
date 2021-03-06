import traceback
from flask import jsonify, request, current_app
from flask.ext import restful

from flask.ext.restful import reqparse


from bitvid.errors import errors, NotFound, PermissionDenied
from bitvid.shared import db, sentry
import traceback

def make_json_error(ex):
    exceptionname = ex.__class__.__name__

    if hasattr(ex, "data"):
        response = jsonify(ex.data)
        response.status_code = 400
        print ex.data
        return response
    else:
        if exceptionname in errors.keys() and exceptionname != "Exception":
            errordata = errors[exceptionname]
        else:
            if current_app.config["DEBUG"]:
                traceback.print_exc()
            else:
                sentry.captureException()
            errordata = errors["Exception"]


        if "message" in errordata.keys():
            response = jsonify(message=str(errordata["message"]))
        else:
            response = jsonify(message=str(ex))

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

        if deletedmodel.user != request.session.user:
            raise PermissionDenied

        db.session.delete(deletedmodel)
        db.session.commit()
        return deletedmodel

    def _put(self, **kwargs):
        changedmodel = self._updateModelFromRequest(
            self.baseModel, kwargs, self.updatefields)
        
        if changedmodel.user != request.session.user:
           raise PermissionDenied

        db.session.add(changedmodel)
        db.session.commit()
        return changedmodel

    def _updateModelFromRequest(self, modelType, searchCriterias, fieldsToUpdate):
        parser = reqparse.RequestParser()
        for field in fieldsToUpdate:
            parser.add_argument(field, required=False, type=str)
        args = parser.parse_args()

        print "found args to update: ", args, "updateFields=", fieldsToUpdate

        model = modelType.query.filter_by(**searchCriterias).first()

        for field in fieldsToUpdate:
            print field, field in args
            if field in args.keys():
                setattr(model, field, args[field])

        return model
