# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name):
    # Initialize app from flask
    app = Flask(__name__)
    db.init_app(app)
    db.app = app

    # Register blueprint
    # Add 'auth' blueprint
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Add directory and error page

    return app

"""
# Local
if __name__ == "__main__":
    create_app(CONFIG).run('127.0.0.1', 5016, debug=True)
"""
if __name__ == "__main__":
    create_app('a').run('0.0.0.0', 8084, debug=True)
