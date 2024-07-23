from flask import url_for

from apps.auth.token import generate_confirmation_token
from apps.email.services import send_single_email

from apps.email.consts import EmailType


def generate_and_send_auth_token(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)

    send_single_email(
        email_type=EmailType.USER_REGISTER_EMAIL,
        context={'confirm_url': confirm_url},
        single_email=email,
    )
