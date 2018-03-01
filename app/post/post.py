from app.post import post
from flask import jsonify
from util.util import query_fetch, query_mod, PostList, query_dict_fetch, ErrorResponse
from instance.config import VERBOSE, DB
from util.util import token_required
from flask import request


###########################################
#                                         #
#            Authorized Code              #
#                                         #
###########################################


def replace(text):
    text = text.lower()
    text = text.replace("'", "''")
    text = text.replace('"', '\"')
    text = text.replace("\\", "\ ")
    text = text.replace("drop", '')
    text = text.replace("select", '')
    text = text.replace('--', '')
    text = text.replace(';', '')
    text = text.replace("delete", '')
    return text

@post.route('/list', methods=['POST'])
@token_required
def get_list():
    offset = int(request.form.get('offset'))
    size = int(request.form.get('size'))
    # offset = (int(temp)+1)*int(size)
    sql = "SELECT pid, title, content, authorid, user_avatar, user_name FROM " \
          "posts INNER JOIN users ON users.user_id = posts.authorid ORDER BY pid DESC LIMIT {} OFFSET {}".format(size, offset)
    if VERBOSE:
        print('get list query:' + sql)
    indicator = query_dict_fetch(sql, DB)
    if indicator:
        response = PostList()
        response.data['offset'] = offset
        response.data['size'] = size
        response.data['count'] = str(len(indicator))
        response.data['postlist'] = indicator
    else:
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = '' #TODO
    return jsonify(response.__dict__)


@post.route('/submit', methods=['POST'])
@token_required
def post_submit():
    post_title = replace((request.form.get('title')).lower())
    post_category = replace((request.form.get('category')).lower())
    post_tags = replace((request.form.get('tags')).lower())
    post_content = replace((request.form.get('content')).lower())
    post_by = request.headers.get('userid')
    if VERBOSE:
        print(post_title, post_category, post_tags, post_content, post_by)

    # No empty title
    if post_title == "":
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = 'title cannot be empty'#TODO

    # No empty content
    elif post_content == "":
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = 'content cannot be empty'#TODO

    # Modify Existing Post
    elif request.form.get('pid') is not None:
        post_id = request.form.get('pid')
        # Check if user_id and post_by matches
        sql = "SELECT authorid FROM posts WHERE pid = '{}'".format(post_id)
        if VERBOSE:
            print(sql)
        indicator = query_fetch(sql, DB)
        user_id = request.headers.get('userid')
        response = PostList()
        if indicator['authorid'] == int(user_id):
            sql = "UPDATE posts SET title='{}', category='{}', tags='{}', content='{}' WHERE pid='{}'".format(post_title, post_category, post_tags, post_content, post_id)
            if VERBOSE:
                print(sql)
            query_mod(sql, DB)
            response.data['pid'] = post_id
    # New Post
    elif request.form.get('pid') is None:
        sql = "INSERT INTO posts(title, content, tags, category, authorid) VALUES ('{}', '{}', '{}', '{}', '{}')" \
            .format(post_title, post_content, post_tags, post_category, post_by)

        if VERBOSE:
            print("insert query:" + sql)
        query_mod(sql, DB)

        # Get the generated post_id
        sql = "SELECT pid FROM posts WHERE category = '{}' AND content = '{}' AND authorid = '{}'" \
            .format(post_category, post_content, post_by)
        if VERBOSE:
            print("get post_id query:" + sql)
        indicator = query_fetch(sql, DB)
        response = PostList()
        if indicator:
            response.data['pid'] = indicator['pid']
    else:
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = 'a'#TODO
    return jsonify(response.__dict__)


@post.route('/get', methods=['POST'])
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
    else:
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = 'Post does not exist'#TODO
    return jsonify(response.__dict__)


@post.route('/delete', methods=['POST'])
@token_required
def post_delete():
    post_by = request.headers.get('userid')
    post_id = request.form.get('pid')
    # Check if requested post exists
    sql = "SELECT * FROM posts WHERE pid='{}'".format(post_id)
    if VERBOSE:
        print("delete post pid check" + sql)
    check = query_fetch(sql, DB)
    if check is None:
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = 'post does not exist'#TODO
        return jsonify(response.__dict__)
    # Check if user have authorization to delete
    sql = "SELECT authorid FROM posts WHERE pid='{}'".format(post_id)
    if VERBOSE:
        print("delete post authorization check" + sql)
    indicator = query_fetch(sql, DB)
    # Authorid and userid matchs and have authority to delete post
    if indicator['authorid'] == int(post_by):
        # Delete the post
        sql = "DELETE FROM posts WHERE authorid = '{}' AND pid = '{}'"\
            .format(post_by, post_id)
        if VERBOSE:
            print("delete post" + sql)
        query_mod(sql, DB)
        response = PostList()
        response.data['pid'] = post_id
    # No authority to delete post
    else:
        response = ErrorResponse()
        response.error['errorCode'] = ''#TODO
        response.error['errorMsg'] = 'No authority'#TODO
    return jsonify(response.__dict__)
