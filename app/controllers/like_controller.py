from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.like_service import like_post, unlike_post, get_post_likes, get_user_likes

like_bp = Blueprint('like', __name__)


@like_bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
def like(post_id):
    user_id = get_jwt_identity()
    result = like_post(user_id, post_id)
    return jsonify(result), result.get('status', 400)


@like_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def unlike(post_id):
    user_id = get_jwt_identity()
    result = unlike_post(user_id, post_id)
    return jsonify(result), result.get('status', 400)


@like_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_likes(post_id):
    user_id = get_jwt_identity()
    result = get_post_likes(post_id, user_id)
    return jsonify(result), result.get('status', 400)


@like_bp.route('/user-likes', methods=['GET'])
@jwt_required()
def get_user_likes_route():
    user_id = get_jwt_identity()
    result = get_user_likes(user_id)

    # Trả về kết quả và status
    return jsonify(result), result.get('status', 400)
