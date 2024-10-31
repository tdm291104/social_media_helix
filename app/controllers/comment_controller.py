from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import create_comment, delete_comment, get_comment, get_post_comments, update_comment, get_user_comments

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.json
    user_id = get_jwt_identity()
    result = create_comment(user_id, data)
    return jsonify(result)

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete(comment_id):
    user_id = get_jwt_identity()
    result = delete_comment(user_id, comment_id)
    return jsonify(result)

@comment_bp.route('/<int:comment_id>', methods=['GET'])
def get(comment_id):
    result = get_comment(comment_id)
    return jsonify(result)

@comment_bp.route('/post/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post_comments_route(post_id):
    result = get_post_comments(post_id)
    return jsonify(result)

@comment_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update(comment_id):
    data = request.json
    user_id = get_jwt_identity()
    result = update_comment(user_id, comment_id, data)
    return jsonify(result)

@comment_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_comments_route(user_id):
    result = get_user_comments(user_id)
    return jsonify(result)