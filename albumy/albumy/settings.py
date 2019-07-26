import os

import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    ALBUMY_ADMIN_EMAIL = os.getenv('EMAIL', '164635470@qq.com')
    ALBUMY_PHOTO_PER_PAGE = 12
    ALBUMY_COMMENT_PER_PAGE = 20
    ALBUMY_NOTIFICATION_PER_PAGE = 20
    ALBUMY_USER_PER_PAGE = 20
    ALBUMY_MANAGE_PHOTO_PER_PAGE = 20
    ALBUMY_MANAGE_USER_PER_PAGE = 30
    ALBUMY_MANAGE_TAG_PER_PAGE = 50
    ALBUMY_MANAGE_COMMENT_PER_PAGE = 30
    ALBUMY_SEARCH_RESULT_PER_PAGE = 20
    ALBUMY_MAIL_SUBJECT_PREFIX = '[Albumy]'

    ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    ALBUMY_PHOTO_SIZE = {'small': 400,
                         'medium':800}
    ALBUMY_PHOTO_SUFFIX = {
        ALBUMY_PHOTO_SIZE['small']:'_s',    #thumbnail
        ALBUMY_PHOTO_SIZE['medium']:'_m',   #display
    }

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    MAX_CONTENT_LENGTH = 3*1024*1024 #文件超3mb返回413

    SQLALCHEMY_TRACK_MODIFICATIONS = False   #是否追踪对象的修改（占额外内存）

    #头像配置
    AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30,100,200)   #头像尺寸

    #邮箱
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Albumy Admin', MAIL_USERNAME)

    #文件上传插件配置flask-Dropzone
    DROPZONE_ALLOWED_FILE_TYPE = 'image'    #允许的文件类型
    DROPZONE_MAX_FILE_SIZE = 3              #文件最大体积，单位mb
    DROPZONE_MAX_FILES = 30                 #单次上传最大数量
    DROPZONE_ENABLE_CSRF = True             #开启csrf保护



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'Albumy-data.db')
    REDIS_URL = "redis://localhost"

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' #in-memory database

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix+os.path.join(basedir,'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}