from datetime import datetime

from flask import redirect, url_for, Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from flask_security import logout_user, login_user, LoginForm, ResetPasswordForm, ForgotPasswordForm, hash_password

from apps import user_datastore
from apps.auth.forms import MyRegisterForm
from apps.database import db
from apps.auth.services import generate_and_send_confirm_token, generate_and_send_reset_token
from apps.auth.token import confirm_token
from apps.email.consts import EMAIL_DATA

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
    email = confirm_token(token, EMAIL_DATA['USER_REGISTER_EMAIL']['purpose'])
    user = user_datastore.find_user(email=current_user.email)
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
        generate_and_send_confirm_token(email=user.email)
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
    generate_and_send_confirm_token(email=current_user.email)
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
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        generate_and_send_reset_token(email=form.email.data)
        flash('Password reset instruction was send to your email.', 'success')
        return redirect(url_for('home.home'))
    return render_template('auth/reset_password.html', form=form)


@module.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    if current_user.is_authenticated:
        flash('You already log in.', 'info')
        return redirect(url_for('home.home'))
    email = confirm_token(token, EMAIL_DATA['USER_FORGOT_PASSWORD_EMAIL']['purpose'])
    if not email:
        flash('Token is expired.', 'warning')
        return redirect(url_for('home.home'))
    form = ResetPasswordForm()
    form.user = user_datastore.find_user(email=email)
    if form.validate_on_submit():
        user = user_datastore.find_user(email=email)
        user.password = hash_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('home.home'))
    return render_template('auth/new_password.html', form=form)
