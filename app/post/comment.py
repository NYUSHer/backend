from app.post import post
from flask import jsonify
from flask import request
from util.util import query_fetch, query_mod, PostList, query_dict_fetch, ErrorResponse
from instance.config import VERBOSE, DB
from util.util import token_required

###########################################
#                                         #
#            Authorized Code              #
#                                         #
###########################################

@token_required
@post.route('/comment/<int:suid>', methods=['GET'])
def get_comments_for_a_user(suid):
    uid = int(request.headers.get("userid"))
    if uid != suid:
        response = ErrorResponse()
        response.error['errorCode'] = '104' # TODO: put it in util
        response.error['errorMsg'] = "You can't not the subscriber!"
        return jsonify(response.__dict__)
    offset = int(request.args.get('offset'))
    size   = int(request.args.get('size'))
    sql = "SELECT * FROM comments WHERE subscriber = {} ORDER BY timestamps DESC LIMIT {} OFFSET {}"\
            .format(suid,size,offset)
    if VERBOSE:
        print('Get comment list query:' + sql)
    indicator = query_dict_fetch(sql, DB)
    if indicator:
        response = PostList()
        response.data['offset'] = offset
        response.data['size'] = size
        response.data['count'] = str(len(indicator))
        response.data['postlist'] = indicator
    else:  # TODO: to be decided, I am not sure it is desirable
        response = ErrorResponse()
        response.error['errorCode'] = 'No comments found.'
        response.error['errorMsg'] = '105' # TODO: put it in util
    return jsonify(response.__dict__)


@token_required
@post.route('/comment', methods=['GET'])
def get_comments_for_a_post():
    offset = int(request.args.get('offset'))
    size   = int(request.args.get('size'))
    pid    = int(request.args.get('pid'))
    sql = "SELECT * FROM comments WHERE pid = {} ORDER BY cid DESC LIMIT {} OFFSET {}" \
        .format(pid, size, offset)
    if VERBOSE:
        print('Get comment list query:' + sql)
    indicator = query_dict_fetch(sql, DB)
    if indicator:
        response = PostList()
        response.data['offset'] = offset
        response.data['size'] = size
        response.data['count'] = str(len(indicator))
        response.data['postlist'] = indicator
    else:  # TODO: to be decided, I am not sure it is desirable
        response = ErrorResponse()
        response.error['errorCode'] = 'No comments found.'
        response.error['errorMsg'] = '105'  # TODO: put it in util
    return jsonify(response.__dict__)

@token_required
@post.route('/comment', methods=['POST'])
def create_a_comment():
    author_id     = int(request.headers.get('userid'))
    subscriber_id = int(request.form.get('suid'))
    pid           = int(request.form.get('pid'))
    content       = request.form.get('content')
    sql = "INSERT INTO comments(content, pid, uid, subscriber) VALUES ('{}', '{}', '{}', '{}')" \
        .format(content, pid, author_id, author_id)
    if VERBOSE:
        print("insert query:" + sql)
    query_mod(sql, DB)
    # Get the generated post_id
    sql = "SELECT cid FROM comments WHERE pid = '{}' AND uid = '{}' AND subscriber = '{}' AND content = '{}'" \
        .format(pid, author_id, subscriber_id, content)
    if VERBOSE:
        print("get post_id query:" + sql)
    indicator = query_fetch(sql, DB)
    response = PostList()
    if indicator:
        response.data['pid'] = indicator['pid']

    else:
        response = ErrorResponse()
        response.error['errorCode'] = '106'  # TODO
        response.error['errorMsg'] = 'Somehow comment is not posted.'  # TODO
        return jsonify(response.__dict__)

@post.route('/comment', methods=['PATCH'])

@post.route('/comment', methods=['DELETE'])

