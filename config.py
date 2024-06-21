import os

from dotenv import load_dotenv

load_dotenv()


class AppConfig(object):
    DEBUG = os.environ['DEBUG']
    CSRF_ENABLED = True
    # Secret key get from previous verify task :)
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO: in future add ProdAppConfig(AppConfig) and LocalAppConfig(AppConfig)
