
from os import getenv
from webapp import create_app
from webapp.extensions import db
from webapp.models import User
from flask.ext.script import Manager

app = create_app(getenv('FLASK_CONFIG') or 'development')

manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)


if __name__ == '__main__':
    manager.run()
