from flask import Blueprint
from flask_login import login_required
from flask_security import roles_accepted

from apps.decorators import confirmed_required

module = Blueprint('user_panel', __name__, url_prefix='/user_panel')


@module.before_request
@login_required
@roles_accepted('user', 'admin')
def before_request():
    pass


@module.route('/user_panel')
@confirmed_required
def user_panel():
    return "user_panel"
