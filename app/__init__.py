from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import config


#db = SQLAlchemy()


def create_app(config_name):
    # Initialize app from flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #db.init_app(app)
    #db.app = app

    # Register blueprint
    # Add 'auth' blueprint
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Add directory and error page

    return app


if __name__ == "__main__":
    create_app('development').run('0.0.0.0', 8084)
