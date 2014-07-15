
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal_with
from flask import request, current_app, redirect


from bitvid.shared import db, generate_token, login_required, videofile_webserver_path
from bitvid.errors import ResourceNotFoundException
from bitvid.tasks import process_video

from bitvid.models.Video import Video


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


class VideoResource(restful.Resource):

    @marshal_with(Video.marshal_fields)
    @login_required
    def put(self, videoID):
        video = Video.query.filter_by(token=videoID).first()

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

        db.session.add(video)
        db.session.commit()

        filelocation = videofile_original_location(videoID, mimetype)
        originalvideofile = open(filelocation, "wb")
        originalvideofile.write(request.data)

        process_video.delay(video.token)
        return video


    def get(selr, videoID, ext, height):
        return redirect(videofile_webserver_path(videoID,height,ext))

def register(api):
    api.add_resource(VideoCollectionResource, "/video/")
    api.add_resource(VideoResource, "/video/<string:videoID>", "/video/<string:videoID>/<string:ext>/<int:height>")
