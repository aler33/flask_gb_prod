import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/alexey/gb_lesson/Flask_g/Flask_gb/blog/blog1.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abcdefg123456"
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = 'cosmo'  # Themes for admin
    OPENAPI_URL_PREFIX = '/api/swagger'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_VERSION = '3.22.1'


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = "sqlite:////home/alexey/gb_lesson/Flask_g/Flask_gb/blog/blog1.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///./blog1.db"
    SECRET_KEY = os.environ.get("SECRET_KEY")
