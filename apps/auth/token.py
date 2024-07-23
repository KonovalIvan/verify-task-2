from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from apps import app
from apps.auth.consts import REGISTER_TOKEN_EXPIRATION_SECONDS


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=REGISTER_TOKEN_EXPIRATION_SECONDS):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return email
    except SignatureExpired:
        return False
