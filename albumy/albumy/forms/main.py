from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Optional, Length, DataRequired


class DescriptionForm(FlaskForm):
    description = TextAreaField('描述', validators=[Optional(), Length(0,500)])
    submit = SubmitField()


class TagForm(FlaskForm):
    tag = StringField('添加标签(用空格隔开)', validators=[Optional(), Length(0,64)])
    submit = SubmitField()

class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField()