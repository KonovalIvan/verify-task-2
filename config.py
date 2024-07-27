import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.prod")


class AppConfig(object):
    DEBUG = os.environ['DEBUG']
    CSRF_ENABLED = True

    # Secret key get from previous verify task :)
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = os.environ['MAIL_USERNAME']

    SESSION_COOKIE_SECURE = True

    SECURITY_REGISTERABLE = False
    SECURITY_PASSWORD_SALT = 'bcrypt'

    USERNAME_ENABLED = False

    SESSION_PERMANENT = os.environ['SESSION_PERMANENT']
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    PERMANENT_SESSION_LIFETIME = int(os.environ['PERMANENT_SESSION_LIFETIME'])
    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.environ['REMEMBER_COOKIE_DURATION_DAYS']))

# TODO: in future add ProdAppConfig(AppConfig) and LocalAppConfig(AppConfig)
