from flask import request, jsonify, abort, url_for, render_template
from flask_mail import Message
from app.auth import auth
from util.util import LOGIN_ERR, REG_ERR, UID_ERR, VERIFY_ERR
from util.util import query_fetch, query_mod, token_required, SuccessResponse, ErrorResponse, time
from util.sendMail import send_mail
from instance.config import VERBOSE, DB, DOMAIN, PORT, PROTOCOL
import uuid


###########################################
#                                         #
#          Non-Authorized Code            #
#                                         #
###########################################
@auth.route('/check', methods=['POST'])
def check_email():
    user_email = request.form.get('email')
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
    if key is None:
        return jsonify(dict(state=False,
                            error={'errorCode': LOGIN_ERR,
                                   'errorMsg': 'User does not exist.'},
                            timestamp=int(time())
                            ))
    elif key['user_key'] is not None:
        return jsonify(dict(state=False,
                            error={'errorCode': VERIFY_ERR,
                                   'errorMsg': 'Verification has not been finished.'},
                            timestamp=int(time())
                            ))

    # user chooses to login by email
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
        response.error['errorMsg'] = "Password is incorrect"
    return jsonify(response.__dict__)


def login_by_email(user_email):
    sql = 'SELECT user_id, user_name FROM users WHERE user_email = "{}"'.format(user_email)
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

        # send email in this block
        verify_url = PROTOCOL + DOMAIN + ':' + str(PORT) + url_for('auth.verify', key=key)
        params = dict(USER=indicator['user_name'], URL=verify_url)
        msg = Message('NYUSHer: Verify Your Login', sender='nyusher@yeah.net', recipients=[user_email])
        msg.html = render_template('login-verification.html', **params)
        send_mail(msg)
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

    sql = 'SELECT user_id FROM users WHERE user_email = "{}"'.format(user_email)
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

        # send email in this block
        verify_url = PROTOCOL +  DOMAIN + ':' + str(PORT) + url_for('auth.verify', key=key)
        params = dict(USER=user_name, USER_EMAIL=user_email, URL=verify_url)
        print(verify_url)
        msg = Message('NYUSHer: Verify Your Email', sender='nyusher@yeah.net', recipients=[user_email])
        msg.html = render_template('email-verification.html', **params)
        send_mail(msg)
    if VERBOSE:
        print(response)
    return jsonify(response.__dict__)


# TODO: not finished
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
        query_mod(sql, DB)
        return render_template('verification-success.html')
    else:
        return render_template('URL-expired.html')


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
    user_id = request.form.get('userid')  # TODO: change api book @jerry
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
    if VERBOSE:
        print(info_2_set)
    for param in info_2_set.keys():
        if param == 'user_pass':
            key = uuid.uuid4()
            sql = "UPDATE users SET user_key = '{}' WHERE user_id = {} " \
                .format(key, user_id)
            query_mod(sql, DB)

            # send email in this block
            sql = 'SELECT user_email, user_name FROM users WHERE user_id = "{}"'.format(user_id)
            info = query_fetch(sql, DB)
            user_name = info['user_name']
            user_email = info['user_email']
            verify_url = PROTOCOL + DOMAIN + ':' + str(PORT) + url_for('auth.verify', key=key)
            params = dict(USER=user_name, URL=verify_url)
            if VERBOSE:
                print(verify_url)
            msg = Message('NYUSHer: Verify Your Password Change', sender='nyusher@yeah.net', recipients=[user_email])
            msg.html = render_template('password-verification.html', **params)
            send_mail(msg)

        sql = "UPDATE users SET {} = '{}' WHERE user_id = {} " \
            .format(param, info_2_set[param], user_id)
        if VERBOSE:
            print(sql)
        query_mod(sql, DB)

    return get_info()
