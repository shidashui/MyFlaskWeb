from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import current_user, login_user, login_required, logout_user

from catchat.extensions import db
from catchat.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(email=email).first()

        if user is not None :
            if user.password_hash is None:
                flash('请使用第三方服务登陆')
                return redirect(url_for('.login'))
            if user.verify_password(password):
                login_user(user, remember_me)
                return redirect(url_for('chat.home'))
        flash('邮箱或密码不正确')
        return redirect(url_for('.login'))
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.home'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('邮箱已存在，请登陆')
            return redirect(url_for('.login'))

        nickname = request.form['nickname']
        password = request.form['password']

        user = User(nickname=nickname, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))
    return render_template('auth/register.html')