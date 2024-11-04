from flask import Blueprint, request, jsonify, session, make_response, current_app
from app.services.auth_service import register_user, login_user, get_account
from app.schemas import UserRegisterSchema
from flask_jwt_extended import decode_token
import jwt
from flask import current_app

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    schema = UserRegisterSchema()
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({'message': str(e), 'status': 400}), 400
    result = register_user(data)
    return jsonify(result)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result = login_user(data)
    return jsonify(result)
