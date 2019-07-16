import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# print(basedir)

WIN = sys.platform.startswith('win')#区分平台
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False  #是否拦截重定向

    SQLALCHEMY_TRACK_MODIFICATIONS = False #是否追踪对象的修改（占额外内存）
    SQLALCHEMY_RECORD_QUERIES = True  #显式地禁用或者启用查询记录

    CKEDITOR_ENABLE_CSRF = True         #是否开启csrf保护
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'  #设置视图函数的url或端点值

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_POST = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Blog Admin', MAIL_USERNAME)

    #('theme name', 'display name')
    BLUELOG_THEMES = {'perfect_blue':'Perfect Blue', 'black_swan':'Black Swan'}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    BLUELOG_ADMIN_EMAIL = '164635470@qq.com'
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_COMMENT_PER_PAGE = 10

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' #in-memory database

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' +os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

