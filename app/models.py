from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_lock = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'about_me': self.about_me,
            'media_url': self.media_url,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'is_lock': self.is_lock
        }

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'media_url': self.media_url,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'media_url': self.media_url,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'created_at': self.created_at.isoformat(),
        }

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    accepted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'follower_id': self.follower_id,
            'followed_id': self.followed_id,
            'accepted': self.accepted,
        }

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'post_id': self.post_id,
        }