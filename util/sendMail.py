from flask_mail import Mail
from flask import current_app
import threading

mail = None


def send_mail(msg):
    app = current_app._get_current_object()
    threading._start_new_thread(send_one_mail, (app, msg))
    print('An email has been sent.')
    return "Sent."


def send_one_mail(app, msg):
    global mail
    with app.app_context():
        if mail is None:
            mail = Mail(app)
        mail.send(msg)
