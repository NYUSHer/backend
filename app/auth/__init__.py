from flask import Blueprint

auth = Blueprint('auth', __name__)

from user import user
auth.register_blueprint(user, url_prefix='/user')