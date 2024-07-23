from datetime import datetime

from flask import redirect, url_for, Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from flask_security import logout_user, login_user, LoginForm, ResetPasswordForm, ForgotPasswordForm, hash_password

from apps import user_datastore
from apps.auth.forms import MyRegisterForm
from apps.auth.models import User
from apps.database import db
from apps.auth.services import generate_and_send_auth_token
from apps.auth.token import confirm_token

module = Blueprint('auth', __name__, url_prefix='/auth')


@module.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        next_page = request.args.get('next') or url_for('home.home')
        flash('Logged in successfully.', 'success')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@module.route("/confirm_email/<token>")
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("core.home"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for('home.home'))


@module.route('/register', methods=['GET', 'POST'])
def register():
    form = MyRegisterForm()
    if form.validate_on_submit():
        user = user_datastore.create_user(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hash_password(form.password.data),
        )
        user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
        db.session.commit()
        generate_and_send_auth_token(email=user.email)
        login_user(user)

        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for('home.home'))
    return render_template('auth/register.html', form=form)


@module.route("/resend_confirm_email")
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("core.home"))
    generate_and_send_auth_token(email=current_user.email)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("home.inactive_account"))


@module.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout in successfully.', 'success')
    return redirect(url_for('home.home'))


@module.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        return redirect(url_for('auth.new_password_test', user_id=user.id))
    return render_template('auth/reset_password.html', form=form)


@module.route('/new_password_test/<user_id>', methods=['GET', 'POST'])
def new_password_test(user_id):
    # TODO: simple logic for tests, change to normal sending and changing password by token from
    #  send_reset_password_instructions()
    form = ResetPasswordForm(user=User.query.get(user_id))
    if form.validate_on_submit():
        form.user.password = hash_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/new_password.html', form=form)


@module.route('/new_password/<user_id>', methods=['GET', 'POST'])
def new_password(user_id):
    pass
