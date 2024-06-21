from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_security import logout_user, login_user
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from apps import user_datastore
from apps.auth.forms import RegisterForm, LoginForm
from apps.auth.models import User
from apps.database import db
from apps.auth.shemas import RegisterSchema, LoginSchema

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
    form = RegisterForm()
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
            flash(ex.messages, 'error')
    return render_template('auth/register.html', form=form)


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
