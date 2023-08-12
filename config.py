import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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


class ProductionConfig(Config):
    ENV = "production"
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
