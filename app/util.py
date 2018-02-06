import pymysql.cursors
from time import time
from flask import request, jsonify
from instance.config import DB

LOGIN_ERR = "001"
REG_ERR = "002"
TOKEN_INVALID = "101"
EMAIL_ERR = "102"
UID_ERR = "103"


def query_mod(sql, config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()


def query_fetch(sql, config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchone()
        connection.commit()
    finally:
        connection.close()
    return result


def auth_required(fn):
    def wrapper(*args, **kwargs):
        user_id = request.form['user_id']
        token = request.form['user_token']
        sql = "SELECT user_tokens FROM users WHERE user_id = '{}'".format(user_id)
        user_token = query_fetch(sql, DB)
        if user_token:
            if token == user_token['user_tokens']:
                return fn(*args, **kwargs)
            else:
                return jsonify(dict(status=False,
                                    error={'errorCode': TOKEN_INVALID,
                                           'errorMsg' : 'Token is invalid'},
                                    timestamp=int(time())
                                    ))
        else:
            return jsonify(dict(status=False,
                                error={'errorCode': UID_ERR,
                                       'errorMsg': 'UID does not exist'},
                                timestamp=int(time())
                                ))
    return wrapper
