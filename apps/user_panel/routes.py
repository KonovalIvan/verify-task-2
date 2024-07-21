from flask import Blueprint


module = Blueprint('user_panel', __name__, url_prefix='/user_panel')


@module.route('/user_panel')
def user_panel():
    return "user_panel"
