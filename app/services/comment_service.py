from app.models import db, User, Post, Comment
from datetime import datetime


def create_comment(user_id, data):
    post_id = data.get('post_id')
    content = data.get('content')

    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}

    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}

    comment = Comment(content=content, user_id=user_id,
                      post_id=post_id, created_at=datetime.utcnow())
    db.session.add(comment)
    db.session.commit()

    return {'message': 'Comment created successfully', 'status': 201}


def delete_comment(user_id, comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return {'message': 'Comment not found', 'status': 404}
    if comment.user_id != user_id:
        return {'message': 'Permission denied', 'status': 403}

    db.session.delete(comment)
    db.session.commit()

    return {'message': 'Comment deleted successfully', 'status': 200}


def delete_comment_by_admin(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return {'message': 'Comment not found', 'status': 404}

    db.session.delete(comment)
    db.session.commit()

    return {'message': 'Comment deleted successfully', 'status': 200}


def get_post_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return {'message': 'Post not found', 'status': 404}

    comments = Comment.query.filter_by(post_id=post_id).all()
    comments = sorted(comments, key=lambda x: x.id, reverse=True)
    return {
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at,
            'user': {
                'id': comment.author.id,
                'username': comment.author.username,
                'avt': comment.author.media_url
            }
        } for comment in comments],
        'status': 200
    }


def get_user_comments(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found', 'status': 404}

    comments = Comment.query.filter_by(user_id=user_id).all()
    return {
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at
        } for comment in comments],
        'status': 200
    }


def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return {'message': 'Comment not found', 'status': 404}

    return {
        'id': comment.id,
        'content': comment.content,
        'created_at': comment.created_at
    }


def update_comment(user_id, comment_id, data):
    comment = Comment.query.get(comment_id)
    if not comment:
        return {'message': 'Comment not found', 'status': 404}
    if comment.user_id != user_id:
        return {'message': 'Permission denied', 'status': 403}

    comment.content = data.get('content')
    db.session.commit()

    return {'message': 'Comment updated successfully', 'status': 200}
