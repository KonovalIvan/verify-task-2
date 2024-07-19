from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MyRegisterForm(RegisterForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    phone = StringField('Phone')
