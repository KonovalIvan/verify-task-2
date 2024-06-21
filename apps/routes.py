from flask import Blueprint

module = Blueprint('home', __name__)


@module.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
