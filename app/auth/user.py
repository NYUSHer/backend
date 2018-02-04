from flask import Blueprint, request, jsonify
from time import time
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from __init__ import app, config
import uuid

user = Blueprint('user', __name__)

@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        response = dict()
        email = request.form['email']
        pwdtoken = request.form['passwdtoken']
        indicator = validate_login(email, pwdtoken)
        if indicator == True:
            cursor = config.cursor()
            query = """SELECT 'user_id' FROM 'users' WHERE 'user_email' = %s"""
            cursor.execute(query, email)
            data_name = cursor.fetchall()
            cursor.close()

            response['state'] = True
            data = dict()
            data['userid'] = data_name
            token = uuid.uuid4()
            data['token'] = token

            # Insert generated token to database
            cursor = config.cursor()
            query = """UPDATE 'users' SET 'user_email' = email WHERE 'user_token' = %s"""
            cursor.execute(query, token)
            cursor.close()
            response['data'] = data
        else:
            response['state'] = False
            error = dict()
            error['errorCode'] =  000# TODO: decide an error code
            error['errorMsg'] = indicator
            response['error'] = error
    response['timestamp'] = int(time())
    return jsonify(response)


@user.route('/register', methods=['POST', 'GET'])
def register():
    response = dict()

    email = request.form['email']
    username = request.form['username']

    # We will examine if email, and username are valid.
    indicator = check_validity(email, username)
    if indicator == True:  # if they are valid
        response['state'] = True
        data = dict()
        cursor = config.cursor()
        token = uuid.uuid4()
        query = """INSERT INTO 'users'('user_name', 'user_email', 'user_tokens') VALUES (%s, %s, %s)"""
        cursor.execute(query, (username, email, token))
        cursor.close()

        data['username'] = username
        data['email'] = email
        data['token'] = token
        response['data'] = data
    else:  # if they are invalid
        response['state'] = False
        error = dict()
        error['errorCode'] =  000# TODO: decide an error code
        error['errorMsg'] = indicator
        response['error'] = error
    response['timestamp'] = time(time())
    return jsonify(response)


@user.route('/avatar', methods=['POST', 'GET'])
def get_avatar():
        """
        TODO: retrieve avatar's url from db
        """
    return imageurl