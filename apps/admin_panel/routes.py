from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_login import login_required
from flask_security import roles_required, hash_password

from apps import user_datastore
from apps.auth.models import User, Role
from apps.database import db
from apps.auth.forms import MyRegisterForm

module = Blueprint('admin_panel', __name__, url_prefix='/admin_panel')


@module.before_request
@login_required
@roles_required('admin')
def before_request():
    pass


@module.route('/admin_panel')
def admin_panel():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin_panel/admin_panel.html', users=users, roles=roles)


@module.route('/delete_user/<user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    user_datastore.delete_user(user)
    db.session.commit()
    flash(f'{user.name} {user.surname} has been deleted', 'success')
    return redirect(request.referrer)


@module.route('/force_create_user', methods=['GET', 'POST'])
def force_create_user():
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
        return redirect(request.referrer)
    return render_template('auth/register.html', form=form)


@module.route('/deactivate/<user_id>')
def deactivate(user_id):
    user = User.query.get(user_id)
    user_datastore.deactivate_user(user)
    db.session.commit()
    flash(f'{user.name} {user.surname} has been deactivated', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/activate/<user_id>')
def activate(user_id):
    user = User.query.get(user_id)
    user_datastore.activate_user(user)
    db.session.commit()
    flash(f'{user.name} {user.surname} has been activated', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/add_permission/<user_id>/<role_name>')
def add_permission(user_id, role_name):
    user = User.query.get(user_id)
    role = user_datastore.find_role(role_name)
    user.roles.append(role)
    db.session.commit()
    flash(f'Permission {role_name} for {user.name} {user.surname} has been added', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/cancel_permission/<user_id>/<role_name>')
def cancel_permission(user_id, role_name):
    user = User.query.get(user_id)
    role = user_datastore.find_role(role_name)
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        flash(f'Permission {role_name} for {user.name} {user.surname} has been removed', 'success')
    else:
        flash(f'Permission {role_name} doesnt exist', 'error')
    return redirect(request.referrer or url_for('home.home'))
