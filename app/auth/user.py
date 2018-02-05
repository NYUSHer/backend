from flask import request, jsonify, redirect, url_for
from time import time
from app.util import CONFIG
from app.auth import auth
import uuid

DEBUG = True

@auth.route('/')
def hi():
    return redirect(url_for('hello'))

@auth.route('/hello')
def hello():
    return "hello"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    response = dict()
    if request.method == 'POST':
        user_email = request.form['email']
        user_token = request.form['passwdtoken']
        if DEBUG:
            print(user_email, user_token)

        # Check of the input email and token match database
        cursor = CONFIG.cursor()
        query = 'SELECT * FROM users WHERE user_email = %s and user_tokens = %s'
        cursor.execute(query, (user_email, str(user_token)))
        indicator = cursor.fetchone()
        print(indicator)
        cursor.close()

        # Login Success
        if indicator:
            print("success")

            cursor = CONFIG.cursor()
            query = "SELECT user_id FROM users WHERE user_email = %s"
            cursor.execute(query, user_email)
            data_name = cursor.fetchall()
            cursor.close()

            response['state'] = True
            data = dict()
            data['userid'] = data_name
            token = uuid.uuid4()
            data['token'] = token

            # Insert generated token to database
            cursor = CONFIG.cursor()
            query = "UPDATE users SET user_email = user_email WHERE user_tokens = %s"
            cursor.execute(query, str(token))
            cursor.close()
            response['data'] = data
        # Login Fail
        else:
            print("fail")
            response['state'] = False
            error = dict()
            error['errorCode'] = 000 # TODO: decide an error code
            error['errorMsg'] = indicator
            response['error'] = error
    response['timestamp'] = int(time())
    return jsonify(response)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    response = dict()
    user_email = request.form['email']
    user_name = request.form['username']
    cursor = CONFIG.cursor()
    # executes query
    query = 'SELECT * FROM users WHERE user_name = %s'
    cursor.execute(query, user_name)
    # stores the results in a variable
    indicator = cursor.fetchone()

    # Invalid (user exists)
    if indicator:
        response['state'] = False
        error = dict()
        error['errorCode'] = 000 # TODO: decide an error code
        error['errorMsg'] = "error"
        response['error'] = error

    # Valid (user doesn't exist)
    else:
        response['state'] = True
        data = dict()
        cursor = CONFIG.cursor()
        user_token = str(uuid.uuid4())
        query = "INSERT INTO users(user_name, user_email, user_tokens) VALUES ('{}', '{}', '{}')".format(user_name, user_email, user_token)
        print(query)
        cursor.execute(query)
        cursor.close()

        data['username'] = user_name
        data['email'] = user_email
        data['token'] = user_token
        response['data'] = data
    response['timestamp'] = int(time())
    return jsonify(response)

"""
@user.route('/avatar', methods=['POST', 'GET'])
def get_avatar():

        #TODO: retrieve avatar's url from db

    return imageurl
"""