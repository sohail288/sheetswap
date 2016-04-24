from wtforms import PasswordField, StringField, validators, Form

import re

EMAIL_RE = r'^[A-Z0-9+_.-]+@[A-Z0-9.-]+$'

class RegistrationForm(Form):
    email = StringField('Email', [validators.InputRequired(),
                                  validators.Regexp(EMAIL_RE, flags=re.IGNORECASE)])
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('check_password', message="Passwords must match")])
    check_password = PasswordField('Retype Password', [validators.InputRequired()])



class LoginForm(Form):
    email = StringField('Email', [validators.Regexp(EMAIL_RE, flags=re.IGNORECASE)])
    password = PasswordField('Password', [validators.InputRequired()])