from flask import Blueprint

widgets = Blueprint('widgets', __name__)

from .bus import *
