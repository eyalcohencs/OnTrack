import logging

from flask import Flask

from update_graph_service.extensions import mail
from update_graph_service.config import Config
from flask_cors import CORS

from update_graph_service.main import bp as main_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True, origins=['http://localhost:4200'])

    # Set logger level
    logging.getLogger().setLevel(logging.INFO)

    # Extensions
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    return app
