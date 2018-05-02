from flask import Flask, render_template
from instance.config import config


def create_app(config_name):
    # Initialize app from flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Register blueprint
    from app.auth import auth as auth_blueprint
    from app.post import post as post_blueprint
    from app.widgets import widgets as widgets_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(post_blueprint, url_prefix='/post')
    app.register_blueprint(widgets_blueprint, url_prefix='/widgets')

    # Add directory and error page

    # Add static page
    @app.route('/favicon.ico/')
    def favicon():
        return 'hello'

    @app.route('/sp.html/')
    def sp():
        return render_template('sp.html')

    @app.route('/bus.html/')
    def bus():
        return render_template('bus.html')

    @app.route('/prof.html/')
    def prof():
        return render_template('prof.html')

    return app


if __name__ == "__main__":
    myApp = create_app('development')
    myApp.run('localhost', 5000, threaded=True)
