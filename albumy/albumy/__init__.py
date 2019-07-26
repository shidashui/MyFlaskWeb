"""
:author: CoderShui
:url: www.phypshui.xyz （好像是)
:copyright:  © 2019 CoderShui <164635470@qq.com>
:license: MIT
"""
import os

import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from albumy.blueprints.auth import auth_bp
from albumy.blueprints.main import main_bp
from albumy.blueprints.user import user_bp
from albumy.extentions import bootstrap, db, mail, moment, login_manager, dropzone, csrf, avatars
from albumy.models import User, Role, Permission, Photo
from albumy.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_template_context(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    dropzone.init_app(app)
    csrf.init_app(app)
    avatars.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role, Permission=Permission,Photo=Photo)


def register_template_context(app):
    pass


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_fount(e):
        return  render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return  render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True,help='先删除后创建')
    def initdb(drop):
        if drop:
            click.confirm('此操作会删除数据库，确认？',abort=True)
            db.drop_all()
            click.echo('删除表')
        db.create_all()
        click.echo('初始化数据库')

    @app.cli.command()
    def init():
        click.echo('正在初始化角色和权限。。。')
        # db.create_all()
        Role.init_role()
        click.echo('ok')

    @app.cli.command()
    @click.option('--user', default=10, help='用户数量，默认10')
    @click.option('--photo', default=30, help='照片数量，默认500')
    def forge(user, photo):
        from albumy.fakes import fake_admin, fake_user,fake_photo

        db.drop_all()
        db.create_all()

        click.echo('初始化角色和权限')
        Role.init_role()
        click.echo('创建管理员')
        fake_admin()
        click.echo('生成用户')
        fake_user(user)
        # click.echo('生成照片。。。')
        # fake_photo(photo)
        click.echo('ok')
