import os

import click
from flask import Flask, render_template, request, jsonify
from flask_login import current_user

from todoism.apis.v1 import api_v1
from todoism.blueprints.auth import auth_bp
from todoism.blueprints.home import home_bp
from todoism.blueprints.todo import todo_bp
from todoism.extensions import db, login_manager, csrf, babel
from todoism.models import Item
from todoism.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_template_context(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    csrf.exempt(api_v1)  #取消对api蓝本的CSRF保护
    babel.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(home_bp)

    app.register_blueprint(api_v1, url_prefix='/api/v1')
    # app.register_blueprint(api_v1, subdomain='api', url_prefix='/v1') #设置子域，如：api.test.com/v1


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除并创建数据库')
    def initdb(drop):
        if drop:
            click.confirm('这项操作会删除数据库，确定继续？', abort=True)
            db.drop_all()
            click.echo('删除数据库')
        db.create_all()
        click.echo('初试化数据库')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors.html', code=400, info='Bad Request'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors.html', code=403, info='Forbbiden'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        #request.host.startwith('api')   http://api.example.com/v1
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html\
            or request.path.startswith('/api'):
            response = jsonify(code=404, message='The requested URL was not fount on the server.')
            response.status_code = 404
            return response
        return render_template('errors.html', code=404, info='Page Not Found'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the requested URL.')
        response.status_code = 405
        return response

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html \
                or request.host.startswith('api'):
            response = jsonify(code=500, message='An internal server error occurred.')
            response.status_code = 500
            return response
        return render_template('errors.html', code=500, info='Server Error'), 500


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            active_items = Item.query.with_parent(current_user).filter_by(done=False).count()
        else:
            active_items = None
        return dict(active_items=active_items)