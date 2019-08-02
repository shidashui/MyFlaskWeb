from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, ValidationError, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, Optional, EqualTo, Email

from albumy.models import User


class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1,30)])
    username = StringField('用户名', validators=[DataRequired(), Length(1,20),
                                              Regexp('^[a-zA-Z0-9]*$', message='用户名只包含a-z, A-Z和0-9')])
    website = StringField('站点', validators=[Optional(), Length(0,255)])
    location = StringField('所在地', validators=[Optional(), Length(0,50)])
    bio = TextAreaField('个人简介', validators=[Optional(), Length(0,120)])
    submit = SubmitField()

    def validate_username(self,field):
        #字段数据  field.data或者form.username.data(在视图实例化用）
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


#头像
class UploadAvatarForm(FlaskForm):
    image = FileField('上传(<=3M)', validators=[FileRequired(),
                                              FileAllowed(['jpg','png'], '文件必须为.jpg或.png格式')])
    submit = SubmitField()

class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并上传')

#密码
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField()

#邮箱
class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1,254), Email()])
    submit =SubmitField()

#消息开关
class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField('新的评论')
    receive_follow_notification = BooleanField('新的关注')
    receive_collect_notification = BooleanField('新的收藏')
    submit = SubmitField()

#隐私设置
class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField('公开收藏')
    submit = SubmitField()


#注销账号
class DeleteAccountForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1,20)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('用户名错误')