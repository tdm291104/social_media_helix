from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db


def register_user(data):
    from app.models import User  # Import trong hàm để tránh circular import

    full_name = data.get('full_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Kiểm tra nếu username hoặc email đã tồn tại
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return {'message': 'User already exists', 'status': 400}

    hashed_password = generate_password_hash(password)
    new_user = User(full_name=full_name, username=username,
                    email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User registered successfully', 'status': 201}


def login_user(data):
    from app.models import User

    username = data.get('username')
    password = data.get('password')

    # Kiểm tra người dùng tồn tại và xác nhận mật khẩu
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        role = user.is_admin
        return {'access_token': access_token, 'message': 'Login successful', 'status': 200, 'role': role}

    return {'message': 'Invalid credentials', 'status': 401}


def get_account(id):
    from app.models import User

    # Kiểm tra người dùng tồn tại và xác nhận mật khẩu
    user = User.query.filter_by(id=id).first()
    if user:
        role = user.is_admin
        return {'role': role, 'message': 'get account successful', 'status': 200}

    return {'message': 'Invalid credentials', 'status': 401}
