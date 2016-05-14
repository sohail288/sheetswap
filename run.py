"""
    Imports App and Runs it
"""

from flask.ext.script import Manager
from flask import g, session, request

from app import get_or_create_app
from app.db import db_session, init_db
from models.auth import User
from util.jinja_filters.jinja_filters import pluralize, time_ago


smtrade = get_or_create_app()
manager = Manager(smtrade)


@smtrade.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@smtrade.before_request
def before_request():
    g.db = db_session()
    if session.get('current_user_id', None) and not request.endpoint == 'testing.server_shutdown':
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


@smtrade.context_processor
def inject_pluralize():
    return dict(pluralize=pluralize)

smtrade.jinja_env.filters['time_ago'] = time_ago


def get_decorated_app():
    return smtrade

if __name__ == "__main__":
    manager.run()
