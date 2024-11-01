from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.follow_service import follow_user, accept_follow_request, delete_follow_request, get_user_followers


follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/<int:target_user_id>', methods=['POST'])
@jwt_required()
def follow(target_user_id):
    user_id = get_jwt_identity()
    result = follow_user(user_id, target_user_id)
    return jsonify(result), result.get('status', 400) # 400 is the default status code

@follow_bp.route('/accept_follow/<int:request_user_id>', methods=['POST'])
@jwt_required()
def accept_follow(request_user_id):
    user_id = get_jwt_identity()
    result = accept_follow_request(user_id, request_user_id)
    return jsonify(result), result.get('status', 400)

@follow_bp.route('/delete_follow/<int:request_user_id>', methods=['DELETE'])
@jwt_required()
def delete_follow_request(request_user_id):
    user_id = get_jwt_identity()
    result = delete_follow_request(user_id, request_user_id)
    return jsonify(result), result.get('status', 400)

#Get followers of user_id
@follow_bp.route('/followers/<int:user_id>', methods=['GET'])
def get_followers(user_id):
    result = get_user_followers(user_id)
    return jsonify(result), result.get('status', 400)