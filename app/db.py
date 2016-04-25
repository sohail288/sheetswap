"""
Sets up the DB and stuff
"""

import os

from flask import request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from . import BASE_DIR




#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db_uri = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
engine = create_engine(db_uri, convert_unicode=True)
db_session  = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine
                                          ))

from .models import Base
Base.query = db_session.query_property()

def init_db(seed_data=False, rebuild=False):
    # import model modules
    import models
    Base.metadata.create_all(bind=engine)

    if rebuild:
        if os.path.exists(db_uri):
            os.remove(db_uri)

    if seed_data:
        from util.seeding_scripts.load_data import load_data
        load_data()






