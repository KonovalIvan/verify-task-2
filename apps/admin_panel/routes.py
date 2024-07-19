from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_login import login_required
from flask_security import roles_required

from apps import user_datastore
from apps.auth.models import User, Role
from apps.database import db

module = Blueprint('admin_panel', __name__, url_prefix='/admin_panel')


@module.route('/admin_panel')
@roles_required('admin')
def admin_panel():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin_panel/admin_panel.html', users=users, roles=roles)


@module.route('/deactivate/<user_id>')
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


@module.route('/add_permission/<user_id>/<role_name>')
@login_required
@roles_required('admin')
def add_permission(user_id, role_name):
    user = User.query.get(user_id)
    role = user_datastore.find_role(role_name)
    user.roles.append(role)
    db.session.commit()
    flash(f'Permission {role_name} for {user.name} {user.surname} has been added', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/cancel_permission/<user_id>/<role_name>')
@login_required
@roles_required('admin')
def cancel_permission(user_id, role_name):
    user = User.query.get(user_id)
    role = user_datastore.find_role(role_name)
    if role in user.roles:
        db.session.refresh(user)
        user.roles.remove(role)
        db.session.commit()
        flash(f'Permission {role_name} for {user.name} {user.surname} has been removed', 'success')
    else:
        flash(f'User {user.name} {user.surname} has not permision {role_name}', 'success')
    return redirect(request.referrer or url_for('home.home'))
