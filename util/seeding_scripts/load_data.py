"""
    Loads data into database.  If the database does not exist, it uses the db modules init_db
    routine to create the db.

    The routine named load_data will be the main routine
"""
import json
import random
from os import path
import uuid

from app.db import db_session, init_db
from app import BASE_DIR
from models.sheets import Sheetmusic, Genre, Instrument
from models.auth   import User, Address
from models.items import Item, ItemImage



DATA_DIRECTORY = path.join(BASE_DIR, 'util/seed_data')

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
                print("added", new_obj)
                db_session.commit()


def load_users():
    with open(path.join(DATA_DIRECTORY, 'auth.json')) as fh:
        data = json.load(fh)

        for user in data['users']:
            if db_session.query(User).filter_by(email=user['email']).one_or_none() is None:
                addresses = user.pop('addresses')

                new_user_obj = User(**user)

                new_address_objs = [Address(**address) for address in addresses]
                new_user_obj.addresses = new_address_objs

                db_session.add(new_user_obj)
                print("added", new_user_obj, new_address_objs)
                db_session.commit()

def load_items(n=50):
    """Load items into DB. The images """
    conditions = ['clean', 'okay', 'torn', 'incomplete']
    description = ["A test description\nThis sheet is cool"]

    sheets = db_session.query(Sheetmusic).all()
    users = db_session.query(User).all()

    random.seed(0)
    for i in range(n):
        sm = random.choice(sheets)
        user = random.choice(users)
        item = Item()
        item.user = user
        item.sheetmusic = sm
        item.condition = random.choice(conditions)
        item.description = random.choice(description)

        # add 4 images to each item
        item.images = [ItemImage("{}_{}".format(user.username, uuid.uuid4())) for i in range(4)]

        db_session.add(item)
        print(item)
        db_session.commit()





def load_data(*args, **kwargs):

    session = db_session()

    load_sheet_music()
    load_users()
    load_items()

    db_session.remove()


