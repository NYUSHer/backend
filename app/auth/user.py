from flask import request, jsonify, abort, url_for
from app.auth import auth
from util.util import LOGIN_ERR, REG_ERR, UID_ERR, verify_err_res
from util.util import query_fetch, query_mod, token_required, SuccessResponse, ErrorResponse
from util.sendMail import send_mail
from instance.config import VERBOSE, DB
import uuid


###########################################
#                                         #
#          Non-Authorized Code            #
#                                         #
###########################################
@auth.route('/check', methods=['POST'])
def check_email():
    user_email = request.form.get.get('email')
    sql = 'SELECT user_id FROM users WHERE user_email = "{}"'.format(user_email)
    indicator = query_fetch(sql, DB)
    if indicator:
        response = SuccessResponse()
    else:
        response = ErrorResponse()
    return jsonify(response.__dict__)


@auth.route('/login', methods=['POST'])
def login():
    user_email = request.form.get('email')
    user_pass = request.form.get('passwdtoken')
    if VERBOSE:
        print(user_email, user_pass)

    # user must finish all verifications to login
    sql = 'SELECT user_key FROM users WHERE user_email = "{}"'.format(user_email)
    key = query_fetch(sql, DB)
    if key is not None:
        return verify_err_res

    if user_pass == "NYUSHer_by_email_login":
        return login_by_email(user_email)
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


def login_by_email(user_email):
    sql = 'SELECT user_id FROM users WHERE user_email = "{}"'.format(user_email)
    indicator = query_fetch(sql, DB)
    # Login Success
    if indicator:
        response = SuccessResponse()
        response.data['userid'] = indicator['user_id']
        token = uuid.uuid4()  # generate token
        key = uuid.uuid4() # generate key
        response.data['token'] = token

        # Insert generated token to database
        sql = "UPDATE users SET user_tokens = '{}', user_key = '{}' WHERE user_id = {} "\
            .format(token, key, indicator['user_id'])
        query_mod(sql, DB)

        # TODO: send email here
        verify_url = 'http://localhost:8084' + url_for('auth.verify', key=key)
        send_mail([user_email], 'verify your login', verify_url)
    # Login Fail
    else:
        response = ErrorResponse()
        response.error['errorCode'] = LOGIN_ERR
        response.error['errorMsg'] = "Email doesn't not exist"
    return jsonify(response.__dict__)


@auth.route('/register', methods=['POST'])
def register():
    user_email = request.form.get('email')
    user_name = request.form.get('username')
    user_pass = request.form.get('passwdtoken')

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
        key = uuid.uuid4()
        sql = "INSERT INTO users(user_name, user_email, user_pass, user_tokens, user_key) VALUES ('{}', '{}', '{}', '{}', '{}')"\
            .format(user_name, user_email, user_pass, user_token, key)
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

        # TODO: send email here
        verify_url = 'http://localhost:8084' + url_for('auth.verify', key=key)
        send_mail([user_email], 'verify your registration', verify_url)
    if VERBOSE:
        print(response)
    return jsonify(response.__dict__)


# TODO: is that alright?
@auth.route('/avatar', methods=['POST'])
def get_avatar():
    user_id = request.form.get('userid')
    sql = 'SELECT user_avatar FROM users WHERE user_id = "{}"'.format(user_id)
    response = query_fetch(sql, DB)
    if response:
        return response['user_avatar']


@auth.route('/verify', methods=['GET'])
@auth.route('/verify/<key>', methods=['GET'])
def verify(key=None):
    if key is None:
        abort(404)
    sql = "SELECT user_key FROM users WHERE user_key = '{}' ".format(key)
    indicator = query_fetch(sql, DB)
    if indicator:
        sql = "UPDATE users SET user_key = null WHERE user_key = '{}' ".format(key)
        query_mod(sql, DB)  # TODO: set expiration date?
        return 'Verification is done!'
    else:
        return 'This url has expired.'


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
    user_id = request.headers.get('userid')
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


@auth.route('/set', methods=['POST'])
@token_required
def set_info():
    user_id = request.headers.get('userid')
    # PAIN IN THE ASS! column name in database does not match api name!! We should fix it someday.
    params = ['username', 'imageuri', 'motto', 'passwdtoken']
    column_names = ['user_name', 'user_avatar', 'user_motto', 'user_pass']  # matching column name
    info_2_set = {}
    for i in range(len(params)):
        data = request.form.get(params[i])
        if data is not None:
            info_2_set[column_names[i]] = data

    for param in info_2_set.keys():
        if param == 'user_pass':
            key = uuid.uuid4()
            sql = "UPDATE users SET user_key = '{}' WHERE user_id = {} " \
                .format(key, user_id)
            query_mod(sql, DB)
            # TODO: send email here
            sql = 'SELECT user_email FROM users WHERE user_id = "{}"'.format(user_id)
            user_email = query_fetch(sql, DB)['user_email']
            verify_url = 'http://localhost:8084' + url_for('auth.verify', key=key)
            send_mail([user_email], 'verify your password change.', verify_url)

        sql = "UPDATE users SET {} = '{}' WHERE user_id = {} " \
            .format(param, info_2_set[param], user_id)
        if VERBOSE:
            print(sql)
        query_mod(sql, DB)

    return 'done'
