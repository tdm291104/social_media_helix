from app.models import Follow, User
from app import db

def follow_user(user_id, target_user_id):
    if user_id == target_user_id:
        return {'message': 'Cannot follow yourself', 'status': 400}

    target_user = User.query.get(target_user_id)
    if not target_user:
        return {'message': 'User not found', 'status': 404}

    follow = Follow.query.filter_by(follower_id=user_id, followed_id=target_user_id).first()
    if follow:
        return {'message': 'Follow request already sent', 'status': 400}

    new_follow = Follow(follower_id=user_id, followed_id=target_user_id, accepted=False)
    db.session.add(new_follow)
    db.session.commit()

    return {'message': 'Follow request sent', 'status': 201}

def accept_follow_request(user_id, request_user_id):
    print(user_id, request_user_id)
    follow_request = Follow.query.filter_by(follower_id=request_user_id, followed_id=user_id).first()
    if not follow_request:
        return {'message': 'Follow request not found', 'status': 404}

    follow_request.accepted = True
    db.session.commit()

    return {'message': 'Follow request accepted', 'status': 200}

def delete_follow_request(user_id, request_user_id):
    follow_request = Follow.query.filter_by(follower_id=request_user_id, followed_id=user_id).first()
    if not follow_request:
        return {'message': 'Follow request not found', 'status': 404}

    db.session.delete(follow_request)
    db.session.commit()

    return {'message': 'Follow request deleted', 'status': 200}

def get_user_followers(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}

    followers = Follow.query.filter_by(followed_id=user_id, accepted=True).all()
    return {
        'followers': [{
            'id': follower.follower_id,
            'username': follower.follower.username,
            'media_url': follower.follower.media_url
        } for follower in followers],
        'status': 200
    }

def get_post_followed(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}
    followers = Follow.query.filter_by(followed_id=user_id, accepted=False).all()
    return {
        'followers': [{
            'id': follower.follower_id,
            'username': follower.follower.username,
            'media_url': follower.follower.media_url
        } for follower in followers],
        'status': 200
    }