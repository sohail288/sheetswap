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

    if rebuild:
        if 'sqlite' in db_uri:
            db_path = db_uri.lstrip('sqlite:')
            if os.path.exists(db_path):
                os.remove(db_path)
        else:
            metadata = get_db_metadata()
            metadata.drop_all()

    Base.metadata.create_all(bind=engine)

    if seed_data:
        from util.seeding_scripts.load_data import load_data
        load_data()

def get_db_metadata(engine=engine):
    metadata = MetaData()
    metadata.bind = engine
    metadata.reflect()
    return metadata


def serialize_all(db_dump_name, tables=None): # this function is not ready
    from sqlalchemy.ext.serializer import dumps
    import pickle
    metadata = get_db_metadata()

    tables = metadata.tables if not tables else tables
    data_dict = {t: dumps(db_session.query(metadata.tables[t]).all())
                    for t in metadata.tables if t in tables}

    file_name = os.path.join(app_settings.BASE_DIR, db_dump_name)
    with open(file_name, 'wb') as fh:
        pickle.dump(data_dict, fh)

def load_all(db_dump_name, tables=None): # this function is not ready
    from sqlalchemy.ext.serializer import loads
    import pickle
    metadata = get_db_metadata()

    file_name = os.path.join(app_settings.BASE_DIR, db_dump_name)
    with open(file_name, 'rb') as fh:
        data_dict = pickle.load(fh)
        for table_name, data in data_dict.items():
            for row in loads(data, metadata, db_session):
                print(row)
                db_session.merge(row)
                db_session.commit()



