from app.models import Post, User, Comment
from app import db
from datetime import datetime
from app.model_toxic_bert import toxic_pipeline

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
    
    # Xóa tất cả các comments liên quan trước
    Comment.query.filter_by(post_id=post_id).delete()

    db.session.delete(post)
    db.session.commit()

    return {'message': 'Post deleted successfully', 'status': 200}


def delete_post_by_admin(post_id):
    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}

    # Xóa tất cả các comments liên quan trước
    Comment.query.filter_by(post_id=post_id).delete()

    db.session.delete(post)
    db.session.commit()

    return {'message': 'Post deleted successfully', 'status': 200}


def get_user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}

    posts = Post.query.filter_by(user_id=user_id).all()
    posts = sorted(posts, key=lambda x: x.id, reverse=True)
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


def get_all_posts():
    posts = Post.query.all()
    posts = sorted(posts, key=lambda x: x.id, reverse=True)
    for post in posts:
        rs = toxic_pipeline(post.content)[0]
        #kiểm tra score toxic
        if rs['score'] > 0.4:
            post.toxic = True
        else:
            post.toxic = False

    return {
        'posts': [{
            'id': post.id,
            'content': post.content,
            'media_url': post.media_url,
            'created_at': post.created_at,
            'author': post.author.username,
            'avatar': post.author.media_url,
            'toxic': post.toxic
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
    # post.media_url = data.get('media_url', post.media_url)
    db.session.commit()

    return {'message': 'Post updated successfully', 'status': 200}


def up():
    print('1')
    print('2')