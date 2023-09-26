from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_caching import Cache

jwt = JWTManager()
mail = Mail()
cache = Cache()
