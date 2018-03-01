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
@post.route('/comment/<int:pid>', methods=['GET'])
def get_comments(pid):
    sql = "SELECT cid, pid, content, subscriber, user_avatar, user_name FROM " \
          "comment INNER JOIN users ON comment.uid = posts.authorid ORDER BY pid DESC LIMIT {} OFFSET {}".format(size,offset)

@post.route('/comment', methods=['POST'])
def get_comments_from_one_user():

@post.route('/comment', methods=['PUT'])

@post.route('/comment', methods=['PATCH'])

@post.route('/comment', methods=['DELETE'])

