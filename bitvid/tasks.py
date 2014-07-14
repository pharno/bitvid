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

celery = make_celery(flask_app)

import time
@celery.task()
def add_together(a, b):
    res = a + b

    time.sleep(5)
    flask_app.logger.info("celery calculated %i" %res)

    return res