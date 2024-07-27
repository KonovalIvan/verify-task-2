from flask import Blueprint, redirect, url_for
from apps.email.services import send_single_email

from apps.email.consts import EmailType

module = Blueprint('email', __name__, url_prefix='/email')


@module.route('/test', methods=['GET', 'POST'])
def email():
    pass
