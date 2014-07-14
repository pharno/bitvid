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
from models.Video import Video
from shared import db

celery = make_celery(flask_app)
db.init_app(flask_app)


@celery.task(name="process_video")
def process_video(videotoken):
    from modules.videoResource import Video
    video = Video.query.filter_by(token = videotoken).first()
    flask_app.logger.info("converting %s"%video)
    return video.title