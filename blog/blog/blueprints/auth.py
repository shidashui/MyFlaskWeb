from flask import Blueprint, redirect, url_for, flash, render_template_string, render_template
from flask_login import login_user, current_user, login_required, logout_user
from blog.models import Admin
from blog.forms import LoginForm
from blog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('欢迎回来', 'info')
                return redirect_back()
            flash('用户名或密码错误','warning')
        else:
            flash('没有用户', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功', 'info')
    return redirect_back()

