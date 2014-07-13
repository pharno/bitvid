__author__ = 'pharno'


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    VIDEO_ORIGINALS_PATH = 'originals/'
    VIDEO_CONVERTED_PATH = 'converted/'
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    CELERY_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = [CELERY_SERIALIZER]
    CELERY_TASK_SERIALIZER = CELERY_SERIALIZER
    CELERY_RESULT_SERIALIZER = CELERY_SERIALIZER
    
class PrdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    VIDEO_STORE_PATH = '/opt/bitvid/data/videos/' # /videos on the bitvid s3 bucket for permanent storage


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.sqlite'
    SERVER_NAME = "local.bitvid.tv:5000"
    VIDEO_STORE_PATH = '/tmp/bitvid/'