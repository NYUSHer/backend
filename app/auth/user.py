from flask import request, jsonify
from time import time
from app.util import CONFIG
from app.auth import auth
from app.util import LOGIN_ERR, REG_ERR, TOKEN_INVALID, EMAIL_ERR, UID_ERR
from app.util import query_fetch, query_mod
import uuid

DEBUG = True


@auth.route('/login', methods=['GET', 'POST'])
def login():
    response = dict()
    if request.method == 'POST':
        user_email = request.form['email']
        user_pass = request.form['passwdtoken']
        if DEBUG:
            print(user_email, user_pass)

        # Check of the input email and token match database
        sql = 'SELECT user_id FROM users WHERE user_email = "{}" and user_pass = "{}"'.format(user_email, user_pass)
        indicator = query_fetch(sql, CONFIG)

        if DEBUG:
            print(indicator)

        # Login Success
        if indicator:
            print("success")
            response['state'] = True
            data = dict()
            data['userid'] = indicator['user_id']
            token = uuid.uuid4() # generate token
            data['token'] = token

            # Insert generated token to database
            sql = "UPDATE users SET user_tokens = '{}' WHERE user_id = {} ".format(token, indicator['user_id'])
            print(sql)
            query_mod(sql, CONFIG)

            response['data'] = data
        # Login Fail
        else:
            print("fail")
            response['state'] = False
            error = dict()
            error['errorCode'] = LOGIN_ERR
            error['errorMsg'] = "Email or Password did not match database"
            response['error'] = error
    response['timestamp'] = int(time())
    print(response)
    return jsonify(response)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    response = dict()
    user_email = request.form['email']
    user_name = request.form['username']
    user_pass = request.form['passwdtoken']

    sql = 'SELECT user_id FROM users WHERE user_name = "{}"'.format(user_name)
    indicator = query_fetch(sql, CONFIG)

    # Invalid (user exists)
    if indicator:
        response['state'] = False
        error = dict()
        error['errorCode'] = REG_ERR
        error['errorMsg'] = "User already exists"
        response['error'] = error

    # Valid (user doesn't exist)
    else:
        response['state'] = True
        data = dict()

        user_token = str(uuid.uuid4())

        sql = "INSERT INTO users(user_name, user_email, user_pass) VALUES ('{}', '{}', '{}')"\
            .format(user_name, user_email, user_pass)
        if DEBUG:
            print("insert query:" + sql)
        query_mod(sql, CONFIG)

        sql = "SELECT user_id FROM users WHERE user_name = '{}'".format(user_name)
        if DEBUG:
            print("get userid query:" + sql)
        user_id = query_fetch(sql, CONFIG)

        data['userid'] = user_id['user_id']
        data['email'] = user_email
        data['username'] = user_name
        data['token'] = user_token
        response['data'] = data

    response['timestamp'] = int(time())
    print(response)
    return jsonify(response)

"""
@user.route('/avatar', methods=['POST', 'GET'])
def get_avatar():

        #TODO: retrieve avatar's url from db

    return imageurl
"""