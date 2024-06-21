import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class AppConfig(object):
    DEBUG = os.environ['DEBUG']
    CSRF_ENABLED = True
    # Secret key get from previous verify task :)
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_PERMANENT = os.environ['SESSION_PERMANENT']
    SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
    PERMANENT_SESSION_LIFETIME = int(os.environ['PERMANENT_SESSION_LIFETIME'])
    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.environ['REMEMBER_COOKIE_DURATION_DAYS']))

# TODO: in future add ProdAppConfig(AppConfig) and LocalAppConfig(AppConfig)
