"""
:author: CoderShui
:url: www.phypshui.xyz （好像是)
:copyright:  © 2019 CoderShui <164635470@qq.com>
:license: MIT
"""
import os

import click
from flask import Flask, render_template

from albumy.extentions import bootstrap, db, mail, moment
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
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


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
        click.echo('正在初始化数据库。。。')
        db.create_all()
        click.echo('ok')

    @app.cli.command()
    def forge():
        pass
