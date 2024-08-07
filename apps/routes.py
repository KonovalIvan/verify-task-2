from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from apps import login_manager, app
from apps.auth.models import User

module = Blueprint('home', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('auth.login') + '?next=' + request.url)
    return response


@module.route("/inactive_account")
@login_required
def inactive_account():
    if current_user.confirmed:
        return redirect(url_for("home.home"))
    return render_template("auth/inactive.html")


@module.route('/home')
@module.route('/')
def home():
    return render_template('index.html', user=current_user)
