from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_security import logout_user
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from apps import user_datastore
from apps.auth.forms import RegisterForm
from apps.database import db
from apps.auth.shemas import RegisterSchema

module = Blueprint('auth', __name__, url_prefix='/auth')


@module.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'


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
            flash(f'Validation error: {ex.messages}', 'error')
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
