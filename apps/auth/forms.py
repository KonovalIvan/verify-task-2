from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

from apps.auth.models import User


class MyRegisterForm(RegisterForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])

    def validate_on_submit(self, extra_validators=None):
        if User.query.filter_by(phone=self.phone.data).first():
            self.phone.errors += (
                'Phone number already used. Please choose a different',
            )
            return False
        return super().validate_on_submit(extra_validators=extra_validators)
