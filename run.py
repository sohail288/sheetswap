"""
    Imports App and Runs it
"""

from flask.ext.script import Manager
from flask import g, session
from app import create_app

from app.db import db_session, init_db

from models.auth import User

smtrade = create_app()
manager = Manager(smtrade)

@smtrade.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@smtrade.before_request
def before_request():
    g.db = db_session()

    if session.get('current_user_id', None):
        g.user = g.db.query(User).filter_by(id=int(session.get('current_user_id'))).first()
    else:
        g.user = None


@smtrade.context_processor
def inject_user():
    if session.get('logged_in', None):
        context = dict(current_user=g.user)
    else:
        context = dict(current_user=None)
    return context

def get_decorated_app():
    return smtrade

if __name__ == "__main__":
    manager.run()
