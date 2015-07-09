import os

basedir = os.path.abspath(os.path.dirname(__file__))


# If you want to store session in redis add this mixin to a config
class RedisMixin(object):
    REDIS = {
        'host': os.environ.get('REDIS_HOST') or 'localhost',
        'port': int(os.environ.get('REDIS_PORT') or 6379),
        'db': int(os.environ.get('REDIS_DB') or 0),
    }


class Development(object):
    DEBUG = True
    # WTF_CSRF_ENABLED = False
    SECRET_KEY = 'hard-to-guess-string'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'development.sqlite')


class Production(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


configs = {
    'development': Development,
    'production': Production,
}
