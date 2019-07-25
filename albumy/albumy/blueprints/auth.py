from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user

from albumy.models import User
from albumy.extentions import db
from albumy.emails import send_confirm_email, send_reset_password_email
from albumy.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from albumy.settings import Operations
from albumy.utils import generate_token, validate_token, redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash('登陆成功', 'info')
            return redirect_back()
        flash('邮箱或密码错误', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功','info')
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email,username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('验证邮件已发送，检查邮箱', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


#邮箱验证
@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('账号已验证', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('无效或者过期的token', 'danger')
        return redirect(url_for('.resend_confrim_email'))

@auth_bp.route('/resend-confrim-email')
@login_required
def resend_confrim_email():
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user,token=token)
    flash('邮件已发送', 'info')
    return redirect(url_for('main.index'))


#重置密码，忘记密码发送邮件在重置
@auth_bp.route('/forget-password', methods=['GET','POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user,operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('重置密码的邮件已发', 'info')
            return redirect(url_for('.login'))
        flash('邮箱错误', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            return redirect(url_for('main.index'))
        if validate_token(user=user,token=token, operation=Operations.RESET_PASSWORD,new_password=form.password.data):
            flash('已修改密码', 'success')
            return redirect(url_for('.login'))
        else:
            flash('链接失效或过期', 'danger')
            return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)