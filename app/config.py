import os

import dotenv


class Config:
    dotenv.load_dotenv()
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 36000
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SESSION_TOKEN_EXPIRATION_IN_DAYS = os.environ.get('SESSION_TOKEN_EXPIRATION_IN_DAYS')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    CACHE_TYPE = 'simple'  # 'redis'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
