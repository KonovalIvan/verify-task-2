from flask import Blueprint, redirect, url_for
from apps.email.services import send_single_email

from apps.email.consts import EmailType

module = Blueprint('email', __name__, url_prefix='/email')


@module.route('/test', methods=['GET', 'POST'])
def email():
    send_single_email(
        email_type=EmailType.USER_REGISTER_EMAIL,
        context={
            "test": "test test test",
            "test2": "test2222222222222222",
        },
        single_email='test@gmail.com'
    )
    return redirect(url_for('home.home'))
