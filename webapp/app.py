
from flask import Flask, render_template
from config import configs
from .extensions import login_manager, db
from .account import account
from .frontend import frontend
from webapp.session import RedisSessionInterface


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    register_session_storage(app, configs[config_name])
    register_blueprints(app)
    init_extensions(app)
    add_error_pages(app)

    return app


def register_session_storage(app, conf):
    if hasattr(conf, 'REDIS'):
        from redis import Redis
        host = conf.REDIS['host']
        port = conf.REDIS['port']
        db_num = conf.REDIS['db']
        app.session_interface = RedisSessionInterface(Redis(host, port, db_num))


def register_blueprints(app):
    app.register_blueprint(frontend)
    app.register_blueprint(account)


def init_extensions(app):
    login_manager.init_app(app)
    db.init_app(app)


def add_error_pages(app):

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
