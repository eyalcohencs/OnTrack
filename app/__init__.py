from flask import Flask
from flask_cors import CORS

from config import DevelopmentConfig
from app.extensions import db, login_manager
from app.main import bp as main_bp
from app.authentication import bp as auth_bp
from app.track import bp as track_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    CORS(app)  # todo - remove before deployment
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(track_bp)

    return app

