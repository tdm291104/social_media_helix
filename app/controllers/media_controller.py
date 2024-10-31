from flask import send_from_directory, Blueprint
import os

media_bp = Blueprint('media', __name__)

@media_bp.route('/media/<path:filename>', methods=['GET'])
def media(filename):
    media_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))
    return send_from_directory(media_folder, filename)