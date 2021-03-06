from celery import Celery
from flask import current_app
import subprocess

from shared import sentry
from baseapp import app as flask_app
from models.Video import Video, ConvertedVideo
from shared import db, videofile_original_location, videofile_converted_location, make_sure_path_exists, thumbnail_location
from Media import Media



def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

db.init_app(flask_app)
sentry.app = flask_app
sentry.init_app(flask_app)

celery = make_celery(flask_app)

from raven.contrib.celery import register_signal

register_signal(sentry)

VideoHeights = [360, 480]  # ,720,1080]
VideoCodecs = ["H.264", "WebM", "FLV"]

codecmapping = {
    "H.264": "avconv -i {origpath} -strict experimental -vf scale={width}:{height} -c:v libx264",
    "WebM": "avconv -i {origpath} -vf scale={width}:{height} -c:v libvpx -b:v 1M -c:a libvorbis",
    "FLV": "avconv -i {origpath} -ar 22050 -ab 32 -f flv -vf scale={width}:{height}"
}

codec_mime_mapping = {
    "H.264": "mp4",
    "WebM": "webm",
    "FLV": "flv"
}

thumbnail_cmd = "avconv -i {origpath} -s {width}x{height} -ss 4 -vframes 1"

@celery.task(name="process_video")
def process_video(videotoken):
    for height in VideoHeights:
        for codec in VideoCodecs:
            transcode_video.delay(videotoken, height, codec)

    thumbnail.delay(videotoken)


@celery.task(name="thumbnail")
def thumbnail(videotoken):
    height = 150
    video = Video.query.filter_by(token=videotoken).first()
    videoMedia = Media(
        videofile_original_location(
            video.token,
            video.originalmime))

    original_info = videoMedia.get_info_video()
    original_height = original_info["height"]

    scaling = original_height / float(height)

    width = int(original_info["width"] / scaling)

    off_by_1 = width % 2

    if off_by_1:
        width -= 1

    outpath = thumbnail_location(videotoken)
    make_sure_path_exists(current_app.config["THUMBNAIL_STORE_PATH"])

    cmd = thumbnail_cmd.format(
        origpath=videoMedia.source_file,
        height=height,
        width=width).split(" ")

    cmd.append(outpath)

    print cmd
    subprocess.check_call(cmd)

@celery.task(name="transcode_video")
def transcode_video(videotoken, height, codec):
    try:
        arguments = codecmapping[codec]
    except KeyError:
        log.error("no transcoding command found for target codec %s" % codec)
        return

    video = Video.query.filter_by(token=videotoken).first()
    videoMedia = Media(
        videofile_original_location(
            video.token,
            video.originalmime))

    original_info = videoMedia.get_info_video()
    original_height = original_info["height"]

    scaling = original_height / float(height)

    width = int(original_info["width"] / scaling)

    off_by_1 = width % 2

    if off_by_1:
        width -= 1

    #outfilename = "{format}_{height}_{name}.{mime}".format(format=codec,height=height,width=width,name=video.token,mime=video.originalmime)
    #outpath = temppath+outfilename
    outpath = videofile_converted_location(
        video.token,
        height,
        codec_mime_mapping[codec])

    print "outpath", outpath
    print "make_sure_path_exists:",current_app.config["VIDEO_STORE_PATH"] + current_app.config["VIDEO_CONVERTED_PATH"]
    make_sure_path_exists(current_app.config["VIDEO_STORE_PATH"] + current_app.config["VIDEO_CONVERTED_PATH"])
    print "make_sure_path_exists"

    cmd = arguments.format(
        origpath=videoMedia.source_file,
        codec=codec,
        height=height,
        width=width).split(" ")

    cmd.append(outpath)

    print cmd
    subprocess.check_call(cmd)

    convertedVideoModel = ConvertedVideo(
        video,
        height,
        codec_mime_mapping[codec])

    db.session.add(convertedVideoModel)
    db.session.commit()
