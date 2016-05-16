"""
    Configuration Parameters
"""
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bananas'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media/images')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff'}

    # emailing
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEFAULT_SEND_FROM = 'noreply@sheetswap.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    dev_uri = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        dev_uri


class TestingConfig(Config):
    TESTING = True
    db_path = 'test-data.sqlite'
    test_uri = 'sqlite:///' + os.path.join(Config.BASE_DIR, db_path)
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        test_uri
    SERVER_NAME = 'localhost:5001'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')


config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}


def get_env_config(app_settings=None):
    app_settings = app_settings or os.environ['APP_SETTINGS']
    return config.get(app_settings)
