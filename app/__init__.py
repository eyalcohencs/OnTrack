from flask import Flask
from flask_cors import CORS
import logging

from app.config import DevelopmentConfig
from app.extensions import db, login_manager, jwt, migrate
from app.main import bp as main_bp
from app.authentication import bp as auth_bp
from app.track import bp as track_bp
from app.user import bp as user_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_url_path='', static_folder='static', template_folder='static')
    app.config.from_object(config_class)

    # TODO - refactor the login section
    # app.logger.setLevel(logging.INFO)
    # # logging.basicConfig(handlers=logging.StreamHandler)
    logging.getLogger().setLevel(logging.INFO)
    # logger = logging.getLogger()
    # console_handler = logging.StreamHandler()
    # logger.addHandler(console_handler)

    # Handle CORS # todo - remove before deployment
    CORS(app, supports_credentials=True, origins=['http://localhost:4200'])

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(track_bp)
    app.register_blueprint(user_bp)

    return app
