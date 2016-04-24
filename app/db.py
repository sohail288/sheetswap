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

engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite'), convert_unicode=True)
db_session  = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine
                                          ))

from .models import Base
Base.query = db_session.query_property()

def init_db():
    # import model modules
    from models.sheets import models
    from models.auth import models
    Base.metadata.create_all(bind=engine)






