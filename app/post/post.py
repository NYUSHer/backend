from app.post import post
from flask import jsonify
from util.util import query_fetch, query_mod, PostList, query_dict_fetch, fetch_all
from instance.config import VERBOSE, DB
from util.util import token_required
from flask import request


###########################################
#                                         #
#            Authorized Code              #
#                                         #
###########################################

@post.route('/list', methods=['POST'])
@token_required
def get_list():
    temp = request.form.get('offset')
    size = request.form.get('size')
    offset = (int(temp)+1)*int(size)
    sql = "SELECT pid, title, content, authorid, user_avatar FROM posts INNER JOIN users ON users.user_id = posts.authorid LIMIT '{}' OFFSET '{}'".format(size, offset)
    if VERBOSE:
        print('get list query:' + sql)
    indicator = query_dict_fetch(sql, DB)
    response = PostList()
    response.data['offset'] = offset
    response.data['size'] = size
    response.data['count'] = len(indicator)
    response.data['postlist'] = indicator
    return jsonify(response.__dict__)


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
    post_by = request.form.get('authorid')
    if VERBOSE:
        print(post_title, post_category, post_tags, post_content, post_by)

    # Modify Existing Post
    if request.form.get('pid') is not None:
        post_id = request.form.get('pid')
        # Check if user_id and post_by matches
        sql = "SELECT authorid FROM posts WHERE pid = '{}'".format(post_id)
        if VERBOSE:
            print(sql)
        indicator = query_fetch(sql, DB)
        user_id = request.headers.get('userid')
        if indicator['authorid'] == str(user_id):
            sql = "UPDATE posts SET title= '{}', category= '{}', tags= '{}', content= '{}' WHERE authorid = '{}'".format(post_title, post_category, post_tags, post_content, post_by)
            if VERBOSE:
                print(sql)
            query_mod(sql, DB)
            response = PostList()
            response.data['pid'] = post_id
            return jsonify(response.__dict__)
    # New Post
    else:
        sql = "INSERT INTO posts(title, content, tags, category, authorid) VALUES ('{}', '{}', '{}', '{}', '{}')" \
            .format(post_title, post_content, post_tags, post_category, post_by)

        if VERBOSE:
            print("insert query:" + sql)
        query_mod(sql, DB)

        # Get the generated post_id
        sql = "SELECT pid FROM posts WHERE category = '{}' AND content = '{}' AND authorid = '{}'"\
            .format(post_category, post_content, post_by)
        if VERBOSE:
            print("get post_id query:" + sql)
        indicator = query_fetch(sql, DB)
        if indicator:
            response = PostList()
            response.data['pid'] = indicator['pid']
            return jsonify(response.__dict__)


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
    post_id = request.form.get('pid')
    sql = "SELECT title, category, tags, content FROM posts WHERE pid = '{}'".format(post_id)
    if VERBOSE:
        print("post get query:" + sql)
    indicator = query_fetch(sql, DB)
    response = PostList()
    if indicator:
        response.data['pid'] = post_id
        response.data['title'] = indicator['title']
        response.data['category'] = indicator['category']
        """
        NOTE: Tags must be deserialized first.
              Split with comma
        e.g. post_tags = 'dog, 2017, happy, weekend'
        """
        response.data['tags'] = indicator['tags']
        response.data['content'] = indicator['content']
        return jsonify(response.__dict__)


@post.route('/delete', methods=['POST'])
@token_required
def post_delete():
    post_by = request.headers.get('authorid')
    post_id = request.data.get('pid')
    sql = "DELETE FROM posts WHERE authorid = '{}' AND pid = '{}'"\
        .format(post_by, post_id)
    if VERBOSE:
        print("delete post" + sql)
    query_mod(sql, DB)
