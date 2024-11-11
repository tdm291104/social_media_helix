from app.models import Like, Post
from app import db

def like_post(user_id, post_id):
    if not Post.query.filter_by(id=post_id).first():
        return {'message': 'Post not found', 'status': 404}
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if like:
        return {'message': 'You already liked this post', 'status': 400}

    new_like = Like(user_id=user_id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()

    return {'message': 'Post liked successfully', 'status': 201}

def unlike_post(user_id, post_id):
    if not Post.query.filter_by(id=post_id).first():
        return {'message': 'Post not found', 'status': 404}
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not like:
        return {'message': 'You have not liked this post', 'status': 400}

    db.session.delete(like)
    db.session.commit()

    return {'message': 'Post unliked successfully', 'status': 200}

def get_post_likes(post_id):
    if not Post.query.filter_by(id=post_id).first():
        return {'message': 'Post not found', 'status': 404}
    likes = Like.query.filter_by(post_id=post_id).all()
    return {
        'likes': [{
            'id': like.user_id,
            'username': like.user.username
        } for like in likes],
        'status': 200
   }