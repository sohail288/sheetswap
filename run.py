"""
    Imports App and Runs it
"""

from flask.ext.script import Manager
from flask import g
from app import create_app

from app.db import db_session, init_db


smtrade = create_app()
manager = Manager(smtrade)

@smtrade.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@smtrade.before_request
def before_request():
    g.db = db_session()


if __name__ == "__main__":
    manager.run()
