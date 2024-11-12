from app.models import Post, User
from app import db
from datetime import datetime


def create_post(data, user_id):
    content = data.get('content')
    media_url = data.get('media_url')

    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}

    post = Post(content=content, media_url=media_url,
                user_id=user_id, created_at=datetime.utcnow())
    db.session.add(post)
    db.session.commit()

    return {'message': 'Post created successfully', 'status': 201}


def delete_post(user_id, post_id):
    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}
    if post.user_id != user_id:
        return {'message': 'Permission denied', 'status': 403}

    db.session.delete(post)
    db.session.commit()

    return {'message': 'Post deleted successfully', 'status': 200}


def delete_post_by_admin(post_id):
    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}

    db.session.delete(post)
    db.session.commit()

    return {'message': 'Post deleted successfully', 'status': 200}


def get_user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}

    posts = Post.query.filter_by(user_id=user_id).all()
    return {
        'posts': [{
            'id': post.id,
            'content': post.content,
            'media_url': post.media_url,
            'created_at': post.created_at
        } for post in posts],
        'status': 200
    }


def get_all_posts():
    posts = Post.query.all()
    return {
        'posts': [{
            'id': post.id,
            'content': post.content,
            'media_url': post.media_url,
            'created_at': post.created_at,
            'author': post.author.username,
            'avatar': post.author.media_url
        } for post in posts],
        'status': 200
    }


def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}

    return {
        'id': post.id,
        'content': post.content,
        'media_url': post.media_url,
        'created_at': post.created_at,
        'author': post.author.username,
        'status': 200
    }


def update_post(post_id, data):
    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}

    post.content = data.get('content', post.content)
    post.media_url = data.get('media_url', post.media_url)
    db.session.commit()

    return {'message': 'Post updated successfully', 'status': 200}
