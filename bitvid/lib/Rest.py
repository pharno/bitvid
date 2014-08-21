from flask.ext.restful import reqparse


def updateModelFromRequest(modelType, searchCriterias, *updateFields):
    parser = reqparse.RequestParser()
    for field in updateFields:
        parser.add_argument(field, required=False, type=str)
    args = parser.parse_args()

    print "found args to update: ", args, "updateFields=", updateFields

    model = modelType.query.filter_by(**searchCriterias).first()

    for field in updateFields:
        print field, field in args
        if field in args.keys():
            setattr(model, field, args[field])

    return model
