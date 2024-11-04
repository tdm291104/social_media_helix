from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()


def create_app():
    print('Creating app...')
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/helix_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config.from_object(Config)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    socketio.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Connected to database! Tables: {tables}")

            # Tạo tất cả các bảng nếu chưa tồn tại
            db.create_all()
            print("Database tables created!")
        except OperationalError as e:
            print(f"Database connect fail: {str(e)}")

    JWTManager(app)
    from .controllers.media_controller import media_bp
    from .controllers.auth_controller import auth_bp
    from .controllers.user_controller import user_bp
    from .controllers.post_controller import post_bp
    from .controllers.follow_controller import follow_bp
    from .controllers.comment_controller import comment_bp
    from .controllers.like_controller import like_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(post_bp, url_prefix='/api/post')
    app.register_blueprint(follow_bp, url_prefix='/api/follow')
    app.register_blueprint(comment_bp, url_prefix='/api/comment')
    app.register_blueprint(like_bp, url_prefix='/api/like')
    app.register_blueprint(media_bp)

    return app
