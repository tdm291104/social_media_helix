from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.follow_service import follow_user, accept_follow_request


follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/follow/<int:target_user_id>', methods=['POST'])
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