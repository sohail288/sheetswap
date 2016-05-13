from flask import render_template, current_app
from flask.ext.mail import Message
from config import get_env_config
from app import celery

app_settings = get_env_config()

@celery.task
def send_mail(to, subject, template, **kwargs):
    """ Borrowed from Flask Web Development """
    from run import mail, smtrade

    with smtrade.test_request_context():
        msg = Message(subject,
                      sender=app_settings.DEFAULT_SEND_FROM, recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)

