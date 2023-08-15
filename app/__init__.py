from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import DevelopmentConfig
from app.extensions import db, login_manager, jwt
from app.main import bp as main_bp
from app.authentication import bp as auth_bp
from app.track import bp as track_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True, origins=['http://localhost:4200'])  # todo - remove before deployment

    # Initialize Flask extensions here
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    jwt.init_app(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(track_bp)

    return app

