import os

import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    CATCHAT_ADMIN_EMAIL = os.getenv('CATCHAT_ADMIN_EMAIL', '164635470@qq.com')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix+os.path.join(basedir, 'chatdata.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CATCHAT_MESSAGE_PER_PAGE = 30

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}