import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 36000


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/postgres'
    # or  os.environ.get('DATABASE_URI')\
    # or 'sqlite:///' + os.path.join(basedir, 'app.db')\
    NEO4J_URI = 'bolt://localhost:7687'
    NEO4J_USERNAME = 'OnRoadLocally'
    NEO4J_PASSWORD = '12345678'
    SECRET_KEY = 'demosecretketfordevelopmentenviroment'
    JWT_SECRET_KEY = 'demojwtsecretkey'
    OSM_KEY_API = '5b3ce3597851110001cf62484b230adacdbc4955bb74ea0a0ee9cc05'


class ProductionConfig(Config):
    ENV = "production"
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
