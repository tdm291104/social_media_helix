from app.models import User, Follow
from app import db

def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}
    
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'full_name': user.full_name,
        'about_me': user.about_me,
        'avatar_url': user.media_url,
        'address': user.address,
        'created_at': user.created_at,
        'status': 200
    }


def update_user_profile(user_id, data):
    print(f"Received data for user {user_id}: {data}")  # In ra dữ liệu nhận được
    user = User.query.get(user_id)
    
    if not user:
        return {'message': 'User not found', 'status': 404}

    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.about_me = data.get('about_me', user.about_me)
    user.media_url = data.get('media_url', user.media_url)
    user.address = data.get('address', user.address)

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error committing to database: {e}")
        return {'message': 'Database error occurred', 'status': 500}

    return {
        'profile': user.to_dict(),
        'message': 'Profile updated successfully',
        'status': 200
    }

def delete_user(user_id):
    if not User.query.get(user_id).is_admin:
        return {'message': 'Unauthorized', 'status': 401}
    
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}
    db.session.delete(user)
    db.session.commit()

    return {'message': 'User deleted successfully', 'status': 200}

def search_user(username):
    users = User.query.filter(User.username.ilike(f'%{username}%')).all()
    if not users:
        return {'message': 'No user found', 'status': 404}
    
    return {
        'users': [user.to_dict() for user in users],
        'status': 200
    }

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'message': 'User not found', 'status': 404}
    
    return {
        'user': user.to_dict(),
        'status': 200
    }

def get_all_users():
    users = User.query.all()
    if not users:
        return {'message': 'No user found', 'status': 404}
    
    return {
        'users': [user.to_dict() for user in users],
        'status': 200
    }

def delete_user_for_admin(user_id, admin_id):
    admin = User.query.get(admin_id)
    if not admin.is_admin:
        return {'message': 'Unauthorized', 'status': 401}
    
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}
    db.session.delete(user)
    db.session.commit()

    return {'message': 'User deleted successfully', 'status': 200}