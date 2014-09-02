
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from flask import request, redirect, current_app


from bitvid.shared import db, login_required, videofile_webserver_path, videofile_original_location, make_sure_path_exists
from bitvid.errors import ResourceNotFoundException, PermissionDenied
from bitvid.tasks import process_video

from bitvid.models.Video import Video, ConvertedVideo
from bitvid.lib import BitVidRestful


class VideoCollectionResource(restful.Resource):

    @marshal_with(Video.marshal_fields_create)
    @login_required
    def post(self):
        # return the temporary video id which is used by the rest client to upload the video file
        # as it is not possible to upload raw json and a file at the same time

        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('description', required=False, type=str)
        args = parser.parse_args()

        newvideo = Video(
            args["title"],
            args["description"],
            request.session.user)
        db.session.add(newvideo)
        db.session.commit()

        print request.session.user.videos

        print newvideo.__dict__
        return newvideo


class VideoResource(BitVidRestful.BitVidRestResource):
    updatefields = ["title", "description"]
    baseModel = Video

    @marshal_with(Video.marshal_fields)
    @login_required
    def put(self, videoID):
        video = Video.query.filter_by(token=videoID).first()
        if video.user is not request.session.user:
            raise PermissionDenied

        if not video:
            raise ResourceNotFoundException()

        parser = reqparse.RequestParser()
        parser.add_argument(
            'Content-Type',
            required=True,
            type=str,
            location='headers')
        args = parser.parse_args()
        mimetype = args["Content-Type"].split("/")[1].strip(".")
        video.originalmime = mimetype

        make_sure_path_exists(current_app.config["VIDEO_STORE_PATH"] + current_app.config["VIDEO_ORIGINALS_PATH"])
        filelocation = videofile_original_location(videoID, mimetype)
        originalvideofile = open(filelocation, "wb")
        originalvideofile.write(request.data)

        db.session.add(video)
        db.session.commit()

        process_video.delay(video.token)
        return video

    @marshal_with(
        {"videos": fields.List(fields.Nested(ConvertedVideo.marshal_fields))})
    def get(self, videoID):
        video = Video.query.filter_by(token=videoID).first()

        return {"videos": video.convertedVideos}

    @login_required
    @marshal_with(Video.marshal_fields)
    def post(self, videoID):
        video = Video.query.filter_by(token=videoID).first()
        if video.user is not request.session.user:
            raise PermissionDenied

        return self._updateModelFromRequest(self.baseModel, {"token":videoID}, self.updatefields)


class VideoMediaResource(restful.Resource):

    def get(self, videoID, ext=None, height=None):
        return redirect(videofile_webserver_path(videoID, height, ext))


def register(api):
    api.add_resource(VideoCollectionResource, "/video/")
    api.add_resource(
        VideoMediaResource,
        "/video/<string:videoID>/<string:ext>/<int:height>")
    api.add_resource(VideoResource, "/video/<string:videoID>")
