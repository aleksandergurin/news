
from __future__ import division

from datetime import datetime
from urlparse import urlparse
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager


class User(db.Model, UserMixin):
    class const:
        username_min_len = 2
        username_max_len = 255
        username_regex = "^[A-Za-z][A-Za-z0-9_.]*$"
        password_min_len = 4
        password_max_len = 255
        email_max_len = 255
        about_max_len = 4096

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(const.username_max_len), unique=True)
    password_hash = db.Column(db.String(const.password_max_len), default='')
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(const.email_max_len))   # optional field
    about = db.Column(db.UnicodeText)                   # optional field

    posts = db.relation("Post", backref="author", lazy=False, order_by="Post.id")
    comments = db.relation("Comment", backref="author", lazy=False, order_by="Comment.id")

    def __set_password(self, password):
        self.password_hash = generate_password_hash(password)

    password = property(fset=__set_password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def created(self):
        return format_timestamp(self.creation_timestamp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    class const:
        title_min_len = 2
        title_max_len = 255
        url_max_len = 2000
        description_max_len = 4096

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(const.title_max_len))
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(const.url_max_len))   # optional field
    description = db.Column(db.UnicodeText)         # optional field
    number_of_comments = db.Column(db.Integer, default=0)

    author_id = db.Column(db.Integer, db.ForeignKey(User.id))

    comments = db.relation("Comment", backref="post", lazy=False, order_by="Comment.id")

    @property
    def created(self):
        return format_timestamp(self.creation_timestamp)

    @property
    def url_hostname(self):
        parse_result = urlparse(self.url)
        return parse_result.hostname


class Comment(db.Model):
    class const:
        test_max_len = 4096

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))

    @property
    def created(self):
        return format_timestamp(self.creation_timestamp)


def format_timestamp(creation_timestamp):
    delta = datetime.utcnow() - creation_timestamp
    if delta.days == 0:
        if delta.seconds < 60:
            return "{} seconds ago".format(delta.seconds)
        elif delta.seconds < 3600:
            return "{} minutes ago".format(delta.seconds // 60)
        else:
            return "{} hours ago".format(delta.seconds // 3600)
    else:
        return "{} days ago".format(delta.days)
