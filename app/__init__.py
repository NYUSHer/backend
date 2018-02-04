# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.util import CONFIG


db = SQLAlchemy()


def create_app(config_name):
    # Initialize app from flask
    app = Flask(__name__)
    #app.config.from_object(CONFIG[config_name])
    #CONFIG[CONFIG].init_app(app)

    db.init_app(app)
    db.app = app

    # Register blueprint
    # Add 'auth' blueprint
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Add directory and error page

    return app


if __name__ == "__main__":
    create_app(CONFIG).run('127.0.0.1', 5013, debug=True)
