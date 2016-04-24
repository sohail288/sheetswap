"""
    Loads data into database.  If the database does not exist, it uses the db modules init_db
    routine to create the db.

    The routine named load_data will be the main routine
"""
import json

from app.db import db_session, init_db
from app import BASE_DIR
from models.sheets import Sheetmusic, Genre, Instrument
from os import path


DATA_DIRECTORY = path.join(BASE_DIR, 'lib/seed_data')

def load_sheet_music():
    with open(path.join(DATA_DIRECTORY, 'sheet_music.json'), 'r') as fh:
        data = json.load(fh)

        for sheet_music in data['sheet_music']:
            if not db_session.query(Sheetmusic).filter_by(title=sheet_music['title']).first():
                instrumentation = sheet_music.pop('instrumentation', None)
                genres          = sheet_music.pop('genre_tags', None)
                new_obj = Sheetmusic(**sheet_music)

                new_obj.parse_tags(instrumentation, Instrument, 'instrumentation')
                new_obj.parse_tags(genres, Genre, 'genre_tags')

                db_session.add(new_obj)
                print(new_obj)
                db_session.commit()

    print(db_session.new)
    if db_session.new or db_session.dirty:
        db_session.commit()


def load_data(*args, **kwargs):

    session = db_session()

    load_sheet_music()

    db_session.remove()


