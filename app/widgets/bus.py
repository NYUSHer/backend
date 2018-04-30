from app.widgets import widgets
from flask import json, Response
from util.widgets_util import *


@widgets.route('/bus')
def get_recent_bus_for_two_direction():
    dorm_campus = get_recent_shuttles(direction=0, howmany=2)
    campus_dorm = get_recent_shuttles(direction=1, howmany=2)
    data = dict(campus2dorm=campus_dorm, dorm2campus=dorm_campus)
    resp = Response()
    resp.data = json.dumps(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
