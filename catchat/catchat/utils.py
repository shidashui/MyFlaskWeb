from flask import flash


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('%s填写出现错误 - %s' % (getattr(form, field).label.text, error))