from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL


class ProfileForm(FlaskForm):
    nickname = StringField('昵称', validators=[DataRequired(), Length(1,64)])
    github = StringField('GitHub', validators=[Optional(), URL(), Length(0, 128)])
    website = StringField('网站', validators=[Optional(), URL(), Length(0,128)])
    bio = TextAreaField('简介', validators=[Optional(), Length(0,120)])