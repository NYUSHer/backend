from flask import request, jsonify
from app.auth import auth
from app.util import LOGIN_ERR, REG_ERR, UID_ERR
from app.util import query_fetch, query_mod, token_required, SuccessResponse, ErrorResponse
from instance.config import VERBOSE, DB
import uuid


###########################################
#                                         #
#          Non-Authorized Code            #
#                                         #
###########################################
@auth.route('/check', methods=['POST'])
def check_email():
    user_email = request.form['email']
    sql = 'SELECT user_id FROM users WHERE user_email = "{}"'.format(user_email)
    indicator = query_fetch(sql, DB)
    if indicator:
        response = SuccessResponse()
    else:
        response = ErrorResponse()
    return jsonify(response.__dict__)


@auth.route('/login', methods=['POST'])
def login():
    user_email = request.form['email']
    user_pass = request.form['passwdtoken']
    if VERBOSE:
        print(user_email, user_pass)

    # Check of the input email and token match database
    sql = 'SELECT user_id FROM users WHERE user_email = "{}" and user_pass = "{}"'.format(user_email, user_pass)
    indicator = query_fetch(sql, DB)
    if VERBOSE:
        print(indicator)

    # Login Success
    if indicator:
        response = SuccessResponse()
        response.data['userid'] = indicator['user_id']
        token = uuid.uuid4() # generate token
        response.data['token'] = token

        # Insert generated token to database
        sql = "UPDATE users SET user_tokens = '{}' WHERE user_id = {} ".format(token, indicator['user_id'])
        query_mod(sql, DB)
    # Login Fail
    else:
        response = ErrorResponse()
        response.error['errorCode'] = LOGIN_ERR
        response.error['errorMsg'] = "Email or Password did not match database"
    return jsonify(response.__dict__)


@auth.route('/register', methods=['POST'])
def register():
    user_email = request.form['email']
    user_name = request.form['username']
    user_pass = request.form['passwdtoken']

    sql = 'SELECT user_id FROM users WHERE user_name = "{}"'.format(user_name)
    indicator = query_fetch(sql, DB)

    # Invalid (user exists)
    if indicator:
        response = ErrorResponse()
        response.error['errorCode'] = REG_ERR
        response.error['errorMsg'] = "User already exists"

    # Valid (user doesn't exist)
    else:
        response = SuccessResponse()
        user_token = uuid.uuid4()
        sql = "INSERT INTO users(user_name, user_email, user_pass, user_tokens) VALUES ('{}', '{}', '{}', '{}')"\
            .format(user_name, user_email, user_pass, user_token)
        if VERBOSE:
            print("insert query:" + sql)
        query_mod(sql, DB)

        sql = "SELECT user_id FROM users WHERE user_name = '{}'".format(user_name)
        if VERBOSE:
            print("get userid query:" + sql)
        user_id = query_fetch(sql, DB)

        response.data['userid'] = user_id['user_id']
        response.data['email'] = user_email
        response.data['username'] = user_name
        response.data['token'] = user_token

    if VERBOSE:
        print(response)
    return jsonify(response.__dict__)


# TODO: redesign avatar api
@auth.route('/avatar', methods=['POST'])
def get_avatar():
    user_id = request.form['userid']
    sql = 'SELECT user_avatar FROM users WHERE user_id = "{}"'.format(user_id)
    response = query_fetch(sql, DB)
    if response:
        return response['user_avatar']

###########################################
#                                         #
#             Authorized Code             #
#                                         #
###########################################


@auth.route('/authtest', methods=['GET', 'POST'])
@token_required
def authtest():
    return 'hello'


@auth.route('/info', methods=['POST'])
@token_required
def get_info():
    user_id = request.headers['userid']
    if VERBOSE:
        print(user_id)

    # retrieve user's info from DB
    sql = 'SELECT user_name, user_email, user_motto, user_avatar ' \
          'FROM users WHERE user_id = "{}" '.format(user_id)
    indicator = query_fetch(sql, DB)
    if VERBOSE:
        print(indicator)

    # User exists
    if indicator:
        response = SuccessResponse()
        response.data['email'] = indicator['user_email']
        response.data['username'] = indicator['user_name']
        response.data['imageuri'] = indicator['user_avatar']
        response.data['motto'] = indicator['user_motto']
    # User does not exist
    else:
        response = ErrorResponse()
        response.error['errorCode'] = UID_ERR
        response.error['errorMsg'] = "User ID does not exist"
    return jsonify(response.__dict__)
