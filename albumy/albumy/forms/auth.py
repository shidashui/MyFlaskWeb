from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from albumy.models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,254),Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegisterForm(FlaskForm):
    name = StringField('姓名',validators=[DataRequired(), Length(1,30)])
    email = StringField('邮箱', validators=[DataRequired(), Length(1,254), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1,20),
                                              Regexp('^[a-zA-Z0-9]*$', message='用户名只能是大小写英文字符，以及数字')])
    password = PasswordField('密码', validators=[DataRequired(),Length(8,128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已存在')


class ForgetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,254), Email()])
    submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,254), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(8,128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField()