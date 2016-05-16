from flask import render_template, current_app
from flask.ext.mail import Message
from config import get_env_config
from app import mail, get_or_create_celery

app_settings = get_env_config()
celery = get_or_create_celery()


@celery.task
def send_mail(to, subject, template, **kwargs):
    """
    :param to: user to send email to
    :param subject: subject of email
    :param template: the template to use for the email
    :param kwargs: any additional keyword arguments for templates
    :return:
    """

    msg = Message(subject,
                  sender=app_settings.DEFAULT_SEND_FROM, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
