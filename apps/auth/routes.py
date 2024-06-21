from flask import redirect, url_for, Blueprint
from flask_security import logout_user

module = Blueprint('auth', __name__, url_prefix='/auth')


@module.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'


@module.route('/register', methods=['GET', 'POST'])
def register():
    return 'register'


@module.route('/account')
def account():
    return "account"


@module.route('/admin_account')
def admin_account():
    return "admin_account"


@module.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.home'))
