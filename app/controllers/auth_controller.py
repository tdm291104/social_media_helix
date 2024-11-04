from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.schemas import UserRegisterSchema

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
