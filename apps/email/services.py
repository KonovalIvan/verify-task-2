from typing import Dict, Any, List

from flask import render_template
from flask_mail import Message

from apps import mail, app
import threading

from apps.email.consts import EmailType, EMAIL_DATA


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_single_email(
        email_type: EmailType,
        context: Dict[str, Any],
        single_email: str,
) -> None:
    _email_data = EMAIL_DATA[email_type]
    # TODO: Add language choose
    # TODO: save moderator or admin email
    _html = render_template(f"email/{_email_data['html_template']}", **context)

    msg = Message(subject=_email_data['subject']['EN'],
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[single_email],
                  html=_html
                  )
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()


def send_bulk_emails(recipients, sender, subject, body):
    with app.app_context():
        with mail.connect() as conn:
            for user in recipients:
                message = body
                subject = subject
                msg = Message(recipients=user,
                              sender=sender,
                              body=message,
                              subject=subject)
                conn.send(msg)
