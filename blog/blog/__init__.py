import os
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from .extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate
from .models import Admin
from .settings import config


# app = Flask(__name__)
# config_name = os.getenv('FLASK_CONFIG', 'development')
# app.config.from_object(config[config_name])

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logging(app) #注册日志处理器
    register_extensions(app) #注册扩展（扩展初始化）
    register_blueprints(app)  #注册蓝图
    register_commands(app)  #注册自定义shell命令
    register_errors(app)  #注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    register_template_context(app) #注册模板上下文处理函数
    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

def register_blueprints(app):
    pass

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):
    pass

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

def register_commands(app):

    @app.cli.command()
    @click.option('--category', default=10, help='分类数量，默认为10')
    @click.option('--post', default=50, help='文章数量，默认为50')
    @click.option('--comment', default=500, help='评论数量，默认500')
    def forge(category, post, comment):
        from .fakes import fake_admin,fake_categories,fake_posts,fake_comments

        db.drop_all()
        db.create_all()
        click.echo('正在生成数据')
        fake_admin()
        fake_categories(category)
        fake_posts(post)
        fake_comments(comment)
        click.echo('完成')

