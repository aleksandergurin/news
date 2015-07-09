
from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.login_view = '/login'

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from flask.ext.mail import Mail
# mail = Mail()

# from flask.ext.babel import Babel
# babel = Babel()

# from flask.ext.migrate import Migrate
# migrate = Migrate()

# from flask.ext.cache import Cache
# cache = Cache()

# from celery import Celery
# celery = Celery()
