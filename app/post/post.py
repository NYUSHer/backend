from app.post import post
from flask import request, jsonify
from app.auth import auth
from util.util import LOGIN_ERR, REG_ERR, UID_ERR
from util.util import query_fetch, query_mod, token_required, SuccessResponse, ErrorResponse
from instance.config import VERBOSE, DB
from util.util import token_required
from flask import request
import uuid


###########################################
#                                         #
#            Authorized Code              #
#                                         #
###########################################

@post.route('/list', methods=['GET'])
@token_required
def get_list():
    pass

"""
NOTE: Tags must be deserialized first
"""


"""
params:
*offset(=0)
*size(=10)

data:
- offset
- size
- count
- postlist
postlist.each => {
        pid: ,
        title: ,
        content: ,
        author: ,
        img: ,
    }
"""

@post.route('/submit', methods=['POST'])
@token_required
def post_submit():
    post_title = request.form.get('title')
    post_category = request.form.get('category')
    post_tags = request.form.get('tags')
    post_content = request.form.get('content')
    post_by = request.headers.get('user_id')
    if VERBOSE:
        print(post_title, post_category, post_tags, post_content)
    sql = "INSERT INTO posts(post_content, post_tags, post_category, post_by) VALUES ('{}', '{}', '{}', '{}')" \
        .format(post_content, post_tags, post_category, post_by)

    if VERBOSE:
        print("insert query:" + sql)
    query_mod(sql, DB)

    # Get the generated post_id
    sql = "SELECT post_id FROM posts WHERE post_category = '{}' AND post_content = '{}' AND post_by = '{}'"\
        .format(post_category, post_content, post_by)
    if VERBOSE:
        print("get post_id query:" + sql)
    post_id = query_fetch(sql, DB)
    if post_id:
        return post_id['post_id']


"""
params:
title
category
tags
content
*pid
如果 pid 被指定, 代表对 post 进行修改, 此时应检查 userid 是否为 authorid

data:
pid
"""

@post.route('/get', methods=['GET'])
@token_required
def post_get():
    pass


"""
params
pid
data
pid
title
category
tags
content
"""

@post.route('/delete', methods=['POST'])
@token_required
def post_delete():
    pass

"""
params:
 pid
nodata
"""