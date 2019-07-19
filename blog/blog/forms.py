from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError, TextAreaField, \
    HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional

from blog.models import Category


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6,128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1,60)])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('主体', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args,**kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('类别已存在')

class CommentForm(FlaskForm):
    author = StringField('名字', validators=[DataRequired(),Length(1,30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1,254)])
    site = StringField('站点', validators=[Optional(), URL(),Length(0,25)])
    body = TextAreaField('评论',validators=[DataRequired()])
    submit = SubmitField()

class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('标题', validators=[DataRequired(), Length(1,30)])
    url = StringField('链接', validators=[DataRequired(), URL(), Length(1,255)])
    submit = SubmitField()


class SettingForm(FlaskForm):
    name = StringField('名字',validators=[DataRequired(), Length(1,30)])
    blog_title = StringField('博客标题', validators=[DataRequired(), Length(1,60)])
    blog_sub_title = StringField('副标题', validators=[DataRequired(), Length(1,100)])
    about = CKEditorField('详情页面', validators=[DataRequired()])
    submit = SubmitField()