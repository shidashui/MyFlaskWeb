from wtforms import StringField, SelectField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email

from albumy.models import Role, User
from albumy.forms.user import EditProfileForm


class EditProfileAdminForm(EditProfileForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    role = SelectField('角色', coerce=int)
    active = BooleanField('状态')
    confirmed = BooleanField('确认状态')
    submit = SubmitField()


    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(email=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')