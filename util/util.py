import pymysql.cursors
from time import time
from flask import request, jsonify, abort
from instance.config import DB

LOGIN_ERR = "001"
REG_ERR = "002"
TOKEN_INVALID = "101"
VERIFY_ERR = "102"
UID_ERR = "103"


class SuccessResponse(object):
    def __init__(self):
        self.state = True
        self.data = {'placeHolder':1}
        self.timestamp = int(time())

    def __str__(self):
        return str(self.__dict__)


class ErrorResponse(object):
    def __init__(self):
        self.state = False
        self.error = {'errorCode': 0, 'errorMsg': 'blank'}
        self.timestamp = int(time())

    def __str__(self):
        return str(self.__dict__)


class PostList(object):
    def __init__(self):
        self.state = True
        self.data = {}

    def __str__(self):
        return str(self.__dict__)


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


def fetch_all(sql, config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Read all records
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result


def query_dict_fetch(sql, config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    return result


def token_required(fn):
    def wrapper(*args, **kwargs):
        user_id = request.headers.get('userid')
        token = request.headers.get('token')
        if user_id is None or token is None:
            abort(401)
        sql = "SELECT user_tokens, user_key FROM users WHERE user_id = '{}'".format(user_id)
        resp = query_fetch(sql, DB)
        print("Verifying...")
        if resp:
            if token == resp['user_tokens'] and resp['user_key'] is None:
                return fn(*args, **kwargs)
            elif resp['user_key'] is not None:
                return jsonify(dict(state=False,
                                    error={'errorCode': VERIFY_ERR,
                                           'errorMsg' : 'The user has not been verified.'},
                                             timestamp=int(time())
                                             ))
            else:
                return jsonify(dict(state=False,
                                    error={'errorCode': TOKEN_INVALID,
                                           'errorMsg' : 'Token is invalid'},
                                    timestamp=int(time())
                                    ))
        else:
            return jsonify(dict(state=False,
                           error={'errorCode': UID_ERR,
                                  'errorMsg': 'UID does not exist'},
                                timestamp=int(time())
                                ))
    wrapper.__name__ = fn.__name__
    return wrapper


# SQL injection mitigation
def replace(text):
    text = text.replace("'", "''")
    text = text.replace('"', '\"')
    text = text.replace("\\", "\\\\")
    text = text.replace('--', '')
    text = text.replace(';', '')
    return text
