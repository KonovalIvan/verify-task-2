from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_login import login_required
from flask_security import logout_user, login_user, roles_required, ChangePasswordForm, PasswordlessLoginForm, LoginForm
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from apps import user_datastore
from apps.auth.forms import MyRegisterForm
from apps.auth.models import User, Role
from apps.database import db
from apps.auth.shemas import RegisterSchema, LoginSchema, NewPasswordSchema

module = Blueprint('auth', __name__, url_prefix='/auth')


@module.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        login_schema = LoginSchema()
        try:
            serialized_data = login_schema.load({
                "email": form.email.data,
                "password": form.password.data
            })
            user = User.query.filter_by(email=serialized_data['email']).first()
            if user and check_password_hash(user.password, serialized_data["password"]) and user.active:
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('home.home'))
            else:
                flash('Invalid username or password.', 'error')
        except ValidationError as ex:
            flash(ex.messages, 'error')
    return render_template('auth/login.html', form=form)


@module.route('/register', methods=['GET', 'POST'])
def register():
    form = MyRegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        register_schema = RegisterSchema()
        try:
            data = register_schema.load(request.form)
            hash_password = generate_password_hash(data['password'])
            user = user_datastore.create_user(
                    name=data['name'],
                    surname=data['surname'],
                    email=data['email'],
                    phone=data['phone'],
                    password=hash_password,
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


@module.route('/account')
def account():
    return "account"


@module.route('/admin_account')
@roles_required('admin')
def admin_account():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('auth/admin_account.html', users=users, roles=roles)


@module.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))


@module.route('/deactivate/<user_id>')
@login_required
@roles_required('admin')
def deactivate(user_id):
    user = User.query.get(user_id)
    user_datastore.deactivate_user(user)
    db.session.commit()
    flash(f'{user.name} {user.surname} has been deactivated', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/activate/<user_id>')
@login_required
@roles_required('admin')
def activate(user_id):
    user = User.query.get(user_id)
    user_datastore.activate_user(user)
    db.session.commit()
    flash(f'{user.name} {user.surname} has been activated', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = PasswordlessLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        if user := User.query.filter_by(email=email).first():
            # TODO: add send mail to reset password
            # send_reset_password_instructions(user)
            return redirect(url_for('auth.new_password_test', user_id=user.id))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@module.route('/new_password_test/<user_id>', methods=['GET', 'POST'])
def new_password_test(user_id):
    # TODO: simple logic for tests, change to normal sending and changing password by token from
    #  send_reset_password_instructions()
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        register_schema = NewPasswordSchema()
        user = User.query.get(user_id)
        try:
            data = register_schema.load(request.form)
            user.password = generate_password_hash(data['password'])
            db.session.commit()
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        except ValidationError as ex:
            flash(ex.messages, 'error')
    return render_template('auth/new_password.html', form=form)


@module.route('/new_password', methods=['GET', 'POST'])
def new_password():
    pass
