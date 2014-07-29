from celery import Celery


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

from baseapp import app as flask_app
from models.Video import Video, ConvertedVideo
from shared import db, videofile_original_location, videofile_converted_location
from Media import Media

import subprocess

celery = make_celery(flask_app)
db.init_app(flask_app)

VideoHeights = [360, 480]  # ,720,1080]
VideoCodecs = ["H.264", "WebM", "FLV"]

codecmapping = {
    "H.264": "avconv -i {origpath} -vf scale={width}:{height} -c:v libx264",
    "WebM": "avconv -i {origpath} -vf scale={width}:{height} -c:v libvpx -b:v 1M -c:a libvorbis",
    "FLV": "avconv -i {origpath} -ar 22050 -ab 32 -f flv -vf scale={width}:{height}"}

codec_mime_mapping = {
    "H.264": "mp4",
    "WebM": "webm",
    "FLV": "flv"
}


@celery.task(name="process_video")
def process_video(videotoken):
    for height in VideoHeights:
        for codec in VideoCodecs:
            transcode_video.delay(videotoken, height, codec)


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

    scaling = original_height / height

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

    cmd = arguments.format(
        origpath=videoMedia.source_file,
        codec=codec,
        height=height,
        width=width).split(" ")

    cmd.append(outpath)

    print cmd
    subprocess.call(cmd)

    convertedVideoModel = ConvertedVideo(
        video,
        height,
        codec_mime_mapping[codec])

    db.session.add(convertedVideoModel)
    db.session.commit()
