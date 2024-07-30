from flask import redirect, url_for, Blueprint, request, flash, render_template
from flask_login import login_required, current_user
from flask_security import roles_required, hash_password

from apps import user_datastore
from apps.admin_panel.forms import UserInfoForm
from apps.auth.models import User, Role
from apps.auth.services import generate_and_send_reset_token
from apps.database import db
from apps.auth.forms import MyRegisterForm

module = Blueprint('admin_panel', __name__, url_prefix='/admin_panel')


# @module.before_request
# @login_required
# @roles_required('admin')
# def before_request():
#     pass


@module.route('/admin_panel')
def admin_panel():
    users = User.query.filter(User.id != current_user.id)
    roles = Role.query.all()
    return render_template('admin_panel/admin_panel.html', users=users, roles=roles)


@module.route('/delete_user/<user_id>')
def delete_user(user_id):
    _user = User.query.get(user_id)
    user_datastore.delete_user(_user)
    db.session.commit()
    flash(f'{_user} has been deleted', 'success')
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
                confirmed=True,
        )
        user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
        db.session.commit()
        return redirect(url_for('admin_panel.admin_panel'))
    return render_template('auth/register.html', form=form)


@module.route('/deactivate/<user_id>')
def deactivate(user_id):
    _user = user_datastore.find_user(id=user_id)
    user_datastore.deactivate_user(_user)
    db.session.commit()
    flash(f'{_user} has been deactivated', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/activate/<user_id>')
def activate(user_id):
    _user = user_datastore.find_user(id=user_id)
    user_datastore.activate_user(_user)
    db.session.commit()
    flash(f'{_user} has been activated', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/add_permission/<user_id>/<role_name>')
def add_permission(user_id, role_name):
    _user = user_datastore.find_user(id=user_id)
    _role = user_datastore.find_role(role_name)
    user_datastore.add_role_to_user(_user, _role)
    db.session.commit()

    flash(f'Permission {role_name} for {_user} has been added', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/cancel_permission/<user_id>/<role_name>')
def cancel_permission(user_id, role_name):
    _user = user_datastore.find_user(id=user_id)
    _role = user_datastore.find_role(role_name)
    user_datastore.remove_role_from_user(_user, _role)
    db.session.commit()

    flash(f'Permission {role_name} for {_user} has been removed', 'success')
    return redirect(request.referrer or url_for('home.home'))


@module.route('/user_manager/<user_id>', methods=['GET', 'POST'])
def user_manager(user_id):
    user = User.query.get_or_404(user_id)
    form = UserInfoForm(obj=user)
    form.user = user
    if form.validate_on_submit():
        print(user)
        form.populate_obj(user)
        db.session.commit()

        flash(f'User {user} has been updated', 'success')
        return redirect(url_for('admin_panel.admin_panel'))
        # return redirect(request.referrer or url_for('user_manager/<user_id>', user_id=user_id))
    return render_template('admin_panel/user_manager.html', form=form)


@module.route('/reset_user_password/<user_email>')
def reset_user_password(user_email):
    generate_and_send_reset_token(email=user_email)
    flash('Password reset instruction was send to your email.', 'success')
    return redirect(request.referrer or url_for('home.home'))
