from flask import Blueprint, request, jsonify
from app.services.post_service import create_post, delete_post, get_post, get_all_posts, get_user_posts, update_post, delete_post_by_admin
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
import os
# from app.model_toxic_bert import toxic_pipeline

post_bp = Blueprint('post', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@post_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.form.to_dict()

    text = data.get('content')
    # if text:
    #     toxic_result = toxic_pipeline(text)
    #     if toxic_result[0]['label'] == 'toxic':
    #         return jsonify({'message': 'Your post is toxic', 'status': 400}), 400

    media_url = None
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            media_folder = os.path.join('app/media', f'user_id_{user_id}')
            os.makedirs(media_folder, exist_ok=True)
            file_path = os.path.join(media_folder, filename)
            file.save(file_path)
            media_url = f'/media/user_id_{user_id}/{filename}'

    result = create_post({**data, 'media_url': media_url}, user_id)
    return jsonify(result), 201


@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete(post_id):
    user_id = get_jwt_identity()
    result = delete_post(user_id, post_id)
    return jsonify(result)

# Delete post by post_id if you are admin


@post_bp.route('/delete/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_admin(post_id):
    user_id = get_jwt_identity()
    if user_id != 1:
        return jsonify({'message': 'You are not admin', 'status': 403})
    result = delete_post_by_admin(post_id)
    return jsonify(result)


@post_bp.route('/<int:post_id>', methods=['GET'])
def get(post_id):
    result = get_post(post_id)
    return jsonify(result)


@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update(post_id):
    data = request.json
    result = update_post(post_id, data)
    return jsonify(result)


@post_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_posts_route(user_id):
    result = get_user_posts(user_id)
    return jsonify(result)


@post_bp.route('/', methods=['GET'])
def get_all_posts_route():
    result = get_all_posts()
    return jsonify(result)
