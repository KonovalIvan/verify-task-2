from flask import url_for

from apps.auth.token import generate_token
from apps.email.services import send_single_email

from apps.email.consts import EmailType, EMAIL_DATA


# TODO: split 2 method in one more 'clean'
def generate_and_send_confirm_token(email):
    email_type = EmailType.USER_REGISTER_EMAIL
    _email_data = EMAIL_DATA[email_type]
    token = generate_token(email, _email_data['purpose'])
    url = url_for("auth.confirm_email", token=token, _external=True)

    send_single_email(
        email_type=email_type,
        context={'url': url},
        single_email=email,
    )


def generate_and_send_reset_token(email):
    email_type = EmailType.USER_FORGOT_PASSWORD_EMAIL
    _email_data = EMAIL_DATA[email_type]

    token = generate_token(email, _email_data['purpose'])
    url = url_for("auth.new_password", token=token, _external=True)

    send_single_email(
        email_type=email_type,
        context={'url': url},
        single_email=email,
    )