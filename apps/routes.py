from flask import Blueprint, render_template
from flask_login import current_user

module = Blueprint('home', __name__)


@module.route('/home')
@module.route('/')
def home():
    return render_template('index.html', user=current_user)
