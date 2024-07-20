from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_login import login_required
from flask_security import logout_user, login_user, LoginForm, ResetPasswordForm, ForgotPasswordForm, hash_password
from marshmallow import ValidationError

from apps import user_datastore, login_manager
from apps.auth.forms import MyRegisterForm
from apps.auth.models import User
from apps.database import db
from apps.auth.shemas import RegisterSchema

module = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@module.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home.home'))
        flash('Invalid username or email.', 'error')
    return render_template('auth/login.html', form=form)


@module.route('/register', methods=['GET', 'POST'])
def register():
    form = MyRegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        register_schema = RegisterSchema()
        try:
            data = register_schema.load(request.form)
            hashed_password = hash_password(data['password'])
            user = user_datastore.create_user(
                    name=data['name'],
                    surname=data['surname'],
                    email=data['email'],
                    phone=data['phone'],
                    password=hashed_password,
            )
            user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
            db.session.commit()
            return redirect(url_for('home.home'))
        except ValidationError as ex:
            form.password_confirm.errors.append(
                    ex.messages
            )
            flash(ex.messages, 'error')
    return render_template('auth/register.html', form=form)


@module.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))


@module.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            return redirect(url_for('auth.new_password_test', user_id=user.id))
        flash('Invalid email.', 'error')
    return render_template('auth/reset_password.html', form=form)


@module.route('/new_password_test/<user_id>', methods=['GET', 'POST'])
def new_password_test(user_id):
    # TODO: simple logic for tests, change to normal sending and changing password by token from
    #  send_reset_password_instructions()
    form = ResetPasswordForm()
    form.user = User.query.get(user_id)
    if request.method == 'POST' and form.validate_on_submit():
        form.user.password = hash_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/new_password.html', form=form)


@module.route('/new_password/<user_id>', methods=['GET', 'POST'])
def new_password(user_id):
    pass
