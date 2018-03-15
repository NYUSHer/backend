from app.post import post
from flask import jsonify, request
from util.util import query_fetch, query_mod, PostList, query_dict_fetch, ErrorResponse
from instance.config import VERBOSE, DB
from util.util import token_required, replace

###########################################
#                                         #
#            Authorized Code              #
#                                         #
###########################################


@post.route('/comment/<int:suid>', methods=['GET'])
@token_required
def get_comments_for_a_user(suid=None):
    uid = int(request.headers.get("userid"))
    if uid != suid:
        response = ErrorResponse()
        response.error['errorCode'] = '104'
        response.error['errorMsg'] = "No authority."
        return jsonify(response.__dict__)
    try:
        offset = int(request.args.get('offset'))
        size   = int(request.args.get('size'))
    except TypeError:
        offset = 0
        size = 20
    sql = "SELECT users.user_name, comments.* FROM comments, users WHERE comments.uid = users.user_id AND" \
          " subscriber LIKE '%{}%' ORDER BY timestamp DESC LIMIT {} OFFSET {}"\
        .format(suid, size, offset)
    if VERBOSE:
        print('Get comment list query:' + sql)
    indicator = query_dict_fetch(sql, DB)
    if indicator:
        response = PostList()
        response.data['offset'] = offset
        response.data['size'] = size
        response.data['count'] = str(len(indicator))
        response.data['postlist'] = indicator
    else:
        response = ErrorResponse()
        response.error['errorCode'] = 'No comments found.'
        response.error['errorMsg'] = '105'
    return jsonify(response.__dict__)


@post.route('/comment', methods=['GET'])
@token_required
def get_comments_for_a_post():
    try:
        offset = int(request.args.get('offset'))
        size   = int(request.args.get('size'))
    except TypeError:
        offset = 0
        size   = 10
    try:
        pid    = int(request.args.get('pid'))
    except TypeError:
        response = ErrorResponse()
        response.error['errorCode'] = 'missing args.'
        response.error['errorMsg'] = '107'
        return jsonify(response.__dict__)
    sql = "SELECT users.user_name, comments.* FROM comments, users " \
          "WHERE users.user_id = comments.uid AND pid = {} ORDER BY cid DESC LIMIT {} OFFSET {}".format(pid, size, offset)
    if VERBOSE:
        print('Get comment list query:' + sql)
    indicator = query_dict_fetch(sql, DB)
    if indicator:
        response = PostList()
        response.data['offset'] = offset
        response.data['size'] = size
        response.data['count'] = str(len(indicator))
        response.data['postlist'] = indicator
    else:
        response = ErrorResponse()
        response.error['errorCode'] = 'No comments found.'
        response.error['errorMsg'] = '105'
    return jsonify(response.__dict__)


@post.route('/comment', methods=['POST'])
@token_required
def create_a_comment():
    author_id     = int(request.headers.get('userid'))
    subscriber_id = request.form.get('suid')
    pid           = int(request.form.get('pid'))
    content       = replace(request.form.get('content'))
    if content.strip() == '':
        # No empty content allowed
        response = ErrorResponse()
        response.error['errorCode'] = '108'
        response.error['errorMsg'] = 'content cannot be empty'
        return jsonify(response.__dict__)
    sql = "INSERT INTO comments(content, pid, uid, subscriber) VALUES ('{}', '{}', '{}', '{}')" \
        .format(content, pid, author_id, subscriber_id)
    if VERBOSE:
        print("insert query:" + sql)
    query_mod(sql, DB)
    # Get the generated comment
    sql = "SELECT users.user_name,comments.* FROM comments, users " \
          "WHERE users.user_id = comments.uid AND pid = {} AND uid = {} AND subscriber = '{}' " \
          "ORDER BY timestamp DESC LIMIT 1" .format(pid, author_id, subscriber_id)
    if VERBOSE:
        print("get post_id query:" + sql)
    indicator = query_fetch(sql, DB)
    response = PostList()
    if indicator:
        print()
        response.data = indicator
    else:
        response = ErrorResponse()
        response.error['errorCode'] = '106'
        response.error['errorMsg'] = 'Somehow comment is not posted.'
    return jsonify(response.__dict__)


@post.route('/comment/<int:cid>', methods=['PATCH'])
@token_required
def edit_a_comment(cid=None):
    uid  = int(request.headers.get('userid'))
    content = replace(request.form.get('content')) # could be a problem
    sql = "SELECT uid FROM comments WHERE cid = '{}'" .format(cid)
    indicator = query_fetch(sql, DB)
    # authentication
    if indicator:
        if uid != indicator['uid']:
            response = ErrorResponse()
            response.error['errorCode'] = '104'
            response.error['errorMsg'] = "No authority."
            return jsonify(response.__dict__)
    else:
        response = ErrorResponse()
        response.error['errorCode'] = '105'
        response.error['errorMsg'] = 'cid does not exist.'
        return jsonify(response.__dict__)

    # modification
    if content.strip() == '':
        # No empty content
        response = ErrorResponse()
        response.error['errorCode'] = '108'
        response.error['errorMsg'] = 'content cannot be empty.'
    sql = "UPDATE comments SET content='{}', timestamp = (CURRENT_TIMESTAMP) WHERE cid='{}'" \
        .format(content, cid)
    if VERBOSE:
        print(sql)
    query_mod(sql, DB)

    # get the changed comment
    sql = "SELECT * FROM comments WHERE cid = '{}'" .format(cid)
    if VERBOSE:
        print("get post_id query:" + sql)
    indicator = query_fetch(sql, DB)
    response = PostList()
    if indicator:
        response.data = indicator
    else:
        response = ErrorResponse()
        response.error['errorCode'] = '106'
        response.error['errorMsg'] = 'Somehow comment is not posted.'
    return jsonify(response.__dict__)


@post.route('/comment/<int:cid>', methods=['DELETE'])
@token_required
def delete_a_comment(cid):
    uid = int(request.headers.get('userid'))
    sql = "SELECT uid FROM comments WHERE cid = '{}'".format(cid)
    indicator = query_fetch(sql, DB)
    # authentication
    if indicator:
        if uid != indicator['uid']:
            response = ErrorResponse()
            response.error['errorCode'] = '104'
            response.error['errorMsg'] = "No authority."
            return jsonify(response.__dict__)
    else:
        response = ErrorResponse()
        response.error['errorCode'] = '105'
        response.error['errorMsg'] = 'cid does not exist.'
        return jsonify(response.__dict__)

    # deletion
    sql = "DELETE FROM comments WHERE cid = '{}'" \
        .format(cid)
    if VERBOSE:
        print("delete post" + sql)
    query_mod(sql, DB)
    response = PostList()
    response.data['cid'] = cid
    return jsonify(response.__dict__)


