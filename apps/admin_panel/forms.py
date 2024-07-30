from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired

from apps import user_datastore
from apps.auth.models import User


class UserInfoForm(FlaskForm):
    user: User

    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    phone = TelField('Phone', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    active = BooleanField('Is active')
    confirmed = BooleanField('Email confirmed')
    phone_confirmed = BooleanField('Phone confirmed')

    submit = SubmitField("Save")

    def validate_on_submit(self, extra_validators=None):
        if not super().validate_on_submit():
            return False
        if user_datastore.find_user(phone=self.phone.data):
            if not self.user or self.user.phone != self.phone.data:
                self.phone.errors += (
                    'Phone number already used. Please choose a different',
                )
                return False
        if user_datastore.find_user(email=self.email.data):
            if not self.user or self.user.email != self.email.data:
                self.email.errors += (
                    'Email already used. Please choose a different',
                )
                return False
        return True
