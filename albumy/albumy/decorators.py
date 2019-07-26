from functools import wraps

from flask import Markup, url_for, flash, redirect, abort
from flask_login import current_user


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先验证账号.'
                '没有收到邮件？'
                '<a class="alert-link" href="%s">重新发送验证邮件</a>'% url_for('auth.resend_confirm_email')
            )
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorated_funtion(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args,**kwargs)
        return decorated_funtion
    return decorator


def admin_required(func):
    return permission_required('ADMINISTER')(func)