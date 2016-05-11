from run import mail
from flask import render_template
from flask.ext.mail import Message
from config import get_env_config

app_settings = get_env_config()

def send_mail(to, subject, template, **kwargs):
    """ Borrowed from Flask Web Development """
    msg = Message(subject,
                  sender=app_settings.DEFAULT_SEND_FROM, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
