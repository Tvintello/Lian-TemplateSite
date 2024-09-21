import os


app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdkfjasgnbmpobhjkw[dffmljdfjgfg]'
    MAX_CONTENT_LENGTH = 2024 * 2024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_SEARCH_RESULTS = 50
    WHOOSH_BASE = os.path.join('instance', 'main.db')

    ##### настройка Flask-Mail ##### 
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    # MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
        "sqlite:///main.db"


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
        "sqlite:///main.db"


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
        "sqlite:///main.db"