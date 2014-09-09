__author__ = 'pharno'


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
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
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    # /videos on the bitvid s3 bucket for permanent storage
    VIDEO_STORE_PATH = '/opt/bitvid/data/videos/'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.sqlite'
    # SERVER_NAME = "local.bitvid.tv"
    VIDEO_STORE_PATH = '/Users/chatz/bitvid/data/videos/'
    SENTRY_DSN = "http://4cf6df4822814cc998239ef2bf973c03:e81312acb5724aec84fb64a839fb3816@localhost:9000/2"


class PLGConfig(DevConfig):
    VIDEO_STORE_PATH = '/home/bitvid/bitvid/data/videos/'
    SERVER_NAME = "cersei-web-2.bitvid.tv:5000"


class TestConfig(DevConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_INDEX = "bitvid-unittest"
