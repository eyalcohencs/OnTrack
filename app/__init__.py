from flask import Flask
from flask_cors import CORS
import logging

from app.config import Config
from app.extensions import db, login_manager, jwt, migrate
from app.main import bp as main_bp
from app.authentication import bp as auth_bp
from app.track import bp as track_bp
from app.user import bp as user_bp


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='', static_folder='static', template_folder='static')
    app.config.from_object(config_class)

    # Set logging level to INFO
    logging.getLogger().setLevel(logging.INFO)

    # Handle CORS
    CORS(app, supports_credentials=True, origins=['http://localhost:4200'])

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # TODO - do I need login manager
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(track_bp)
    app.register_blueprint(user_bp)

    return app
