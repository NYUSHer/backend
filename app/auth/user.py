from flask import request, jsonify
from time import time
from app.util import CONFIG
from app.auth import auth
from app.util import LOGIN_ERR, REG_ERR, TOKEN_INVALID, EMAIL_ERR, UID_ERR
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
        cursor = CONFIG.cursor()
        query = 'SELECT * FROM users WHERE user_email = "{}" and user_pass = "{}"'.format(user_email, user_pass)
        cursor.execute(query)
        indicator = cursor.fetchone()
        print(indicator)
        cursor.close()

        # Login Success
        if indicator:
            print("success")
            cursor = CONFIG.cursor()
            query = "SELECT user_id FROM users WHERE user_email = '{}'".format(user_email)
            cursor.execute(query)
            data_name = cursor.fetchone()
            cursor.close()

            response['state'] = True
            data = dict()
            data['userid'] = data_name["user_id"]
            token = uuid.uuid4()
            data['token'] = token

            # Insert generated token to database
            cursor = CONFIG.cursor()
            query = "UPDATE users SET user_email = '{}' WHERE user_tokens = '{}'".format(user_email, token)
            cursor.execute(query)
            cursor.close()
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
    cursor = CONFIG.cursor()
    # executes query
    query = 'SELECT * FROM users WHERE user_name = "{}"'.format(user_name)
    cursor.execute(query)
    # stores the results in a variable
    indicator = cursor.fetchone()

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
        cursor = CONFIG.cursor()
        user_token = str(uuid.uuid4())
        query = "INSERT INTO users(user_name, user_email, user_pass) VALUES ('{}', '{}', '{}')".format(user_name, user_email, user_pass)
        print("insert query:" + query)
        cursor.execute(query)
        cursor.close()

        cursor = CONFIG.cursor()
        query = "SELECT user_id FROM users WHERE user_name = '{}'".format(user_name)
        print("get userid query:" + query)
        cursor.execute(query)
        user_id = cursor.fetchone()
        cursor.close()

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