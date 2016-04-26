"""
Sets up the DB and stuff
"""

import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_env_config


app_settings = get_env_config()

db_uri = app_settings.SQLALCHEMY_DATABASE_URI
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

def get_db_metadata(engine=engine):
    metadata = MetaData()
    metadata.bind = engine
    metadata.reflect()
    return metadata






