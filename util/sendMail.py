from flask_mail import Message, Mail
from flask import current_app
from flask import request, jsonify
import threading
from app.post import post
from app.util import query_fetch, query_mod, token_required, SuccessResponse, ErrorResponse


mail = None


@post.route('/sendmail', methods=['GET', 'POST'])
@token_required
def send_mail():
    mail_subject = request.form['subject']
    mail_recip = request.form['recipient']
    mail_content = request.form['content']
    msg = Message(mail_subject, sender='nyusher@yeah.net', recipients=mail_recip)
    msg.body = mail_content
    app = current_app._get_current_object()
    threading._start_new_thread(send_one_mail, (app, msg))
    print("Email sent")
    return "Sent."


def send_one_mail(app, msg):
    global mail
    with app.app_context():
        if mail == None:
            mail = Mail(app)
        mail.send(msg)