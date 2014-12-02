__author__ = 'pharno'

import os

db = None
try:
    os.environ['RDS_DB_NAME']

    db = "mysql://{user}:{password}@{host}:{port}/{name}".format(
        name = os.environ['RDS_DB_NAME'],
        user = os.environ['RDS_USERNAME'],
        password = os.environ['RDS_PASSWORD'],
        host = os.environ['RDS_HOSTNAME'],
        port = os.environ['RDS_PORT']
        )
except:
    db = 'sqlite:///../database.sqlite'


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = db
    VIDEO_ORIGINALS_PATH = 'originals/'
    VIDEO_CONVERTED_PATH = 'converted/'
    CELERY_BROKER_URL = 'redis://localhost:6379',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = [CELERY_SERIALIZER]
    CELERY_TASK_SERIALIZER = CELERY_SERIALIZER
    CELERY_RESULT_SERIALIZER = CELERY_SERIALIZER
    ELASTICSEARCH_URL = "http://localhost:9200/"
    ELASTICSEARCH_INDEX = "bitvid"
    SENTRY_DSN = ""


class PrdConfig(Config):
    # /videos on the bitvid s3 bucket for permanent storage
    VIDEO_STORE_PATH = '/opt/bitvid/data/videos/'


class DevConfig(Config):
    DEBUG = True
    VIDEO_STORE_PATH = '/Users/chatz/bitvid/data/videos/'
    THUMBNAIL_STORE_PATH = '/Users/chatz/bitvid/data/thumbs/'
    SENTRY_DSN = "http://2ea39eb36b0f459280a55a342e6190ef:212f3a69eac347bd98fffd5f17751b74@localhost:9000/2"


class PLGConfig(DevConfig):
    VIDEO_STORE_PATH = '/home/bitvid/bitvid/data/videos/'
    THUMBNAIL_STORE_PATH = '/home/bitvid/bitvid/data/thumbs/'
    SENTRY_DSN = "http://025e997a65724f94ace3f1a931b2c196:fed759b252b342e38ac8e3c25488f84f@cersei-web-2.bitvid.tv:9000/2"


class TestConfig(DevConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_INDEX = "bitvid-unittest"
