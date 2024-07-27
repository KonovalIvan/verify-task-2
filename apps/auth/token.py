from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from flask import current_app
from apps.auth.consts import TOKEN_EXPIRATION_SECONDS


def generate_token(email, purpose):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'] + purpose)


def confirm_token(token, purpose, expiration=TOKEN_EXPIRATION_SECONDS):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'] + purpose,
            max_age=expiration
        )
        return email
    except SignatureExpired:
        return False
