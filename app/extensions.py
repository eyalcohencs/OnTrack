from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache


db = SQLAlchemy()

migrate = Migrate()

login_manager = LoginManager()

jwt = JWTManager()

mail = Mail()

cache = Cache()
