from flask import Blueprint, render_template, current_app, jsonify, make_response
from flask_login import current_user

from todoism.extensions import db

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/intro')
def intro():
    return render_template('_intro.html')



@home_bp.route('/set-locale/<locale>')
def set_locale(locale):
    if locale not in current_app.config['TODOISM_LOCALES']:
        return jsonify(message='Invalid locale'), 404

    response = make_response(jsonify(message='Setting updated.'))
    if current_user.is_authenticated:
        current_user.locale = locale
        db.session.commit()
    else:
        #匿名用户的locale设置保存到cookie中,保存30天
        response.set_cookie('locale', locale, max_age=60*60*24*30)