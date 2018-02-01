from flask import Blueprin, request, jsonify
from time import time

user = Blueprint('user', __name__)

@user.route('/login', methods=['POST', 'GET'])
def login():
    response = dict()
    response['timestamp'] = int(time())
    indicator = validate_login(
        request.form['email'], request.form['passwdtoken'])
    if indicator == True:
        response['state'] = True
        data = dict()
        data['userid'] =  # TODO: retrieve userid from db
        data['token'] =  # TODO: generate token
        response['data'] = data
    else:
        response['state'] = False
        error = dict()
        error['errorCode'] =  # TODO: decide an error code
        error['errorMsg'] = indicator
        response['error'] = error
    return jsonify(response)


@user.route('/register', methods=['POST', 'GET'])
def register():
    response = dict()
    response['timestamp'] = time(time())

    email = request.form['email']
    username = request.form['username']
    passwdtoken = request.form['passwdtoken']

    # We will examine if email, username and passwdtoken are valid.
    indicator = check_validity(email, username, passwdtoken)
    if indicator == True:  # if they are valid
        response['state'] = True
        data = dict()
        """
        TODO: log user response into db
        """
        data['username'] = 'jack' # TODO:
        data['email'] = 'jack@nyu.edu'# TODO:
        data['userid'] = 1  # TODO
        data['token'] =  # TODO
        response['data'] = data
    else:  # if they are invalid
        response['state'] = False
        error = dict()
        error['errorCode'] =  # TODO: decide an error code
        error['errorMsg'] = indicator
        response['error'] = error

    return jsonify(response)


@user.route('/avatar', methods=['POST', 'GET'])
def get_avatar():
        """
        TODO: retrieve avatar's url from db
        """
    return imageuri