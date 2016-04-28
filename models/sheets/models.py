
"""
    Models for sheet music
"""


from sqlalchemy import Table, Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.models import Base
from models.items import Item


SheetmusicGenres = Table('sheetmusic_genres', Base.metadata,
                         Column('sheetmusic_id', Integer, ForeignKey('sheetmusic.id')),
                         Column('genre_id', Integer, ForeignKey('genres.id'))
)

SheetmusicInstruments = Table('sheetmusic_instruments', Base.metadata,
                              Column('sheetmusic_id', Integer, ForeignKey('sheetmusic.id')),
                              Column('instrument_id', Integer, ForeignKey('instruments.id'))
)

class Sheetmusic(Base):
    __tablename__ = "sheetmusic"

    title = Column(Unicode(255), unique=True)
    cover = Column(Unicode(255), unique=True)
    composer = Column(Unicode(255))
    arranged_by = Column(Unicode(255))
    #key = Column(Unicode(8))

    time_signature = Column(Unicode(64))

    genre_tags =  relationship('Genre',
                               secondary=SheetmusicGenres,
                               back_populates='sheetmusic')
    instrumentation = relationship('Instrument',
                                   secondary=SheetmusicInstruments,
                                   back_populates='sheetmusic')

    items = relationship('Item', back_populates='sheetmusic')

    def __init__(self,  *args, **kwargs):
        """ Take the instrumentation and genre_tags kwarg and use parse on them
            Handles the rest of the kwargs normally
        """
        instrumentation_string = kwargs.pop('instrumentation', None)
        genre_string           = kwargs.pop('genre_tags', None)

        if instrumentation_string:
            self.parse_tags(instrumentation_string, Instrument, 'instrumentation')

        if genre_string:
            self.parse_tags(genre_string, Genre, 'genre_tags')

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)




    def __repr__(self):
        return '<Sheetmusic id={} title={} composer={}>'.format(
            self.id,
            self.title,
            self.composer
        )

    def parse_tags(self, tag_string, TagObj, rel):
        tag_set = set(tag.strip().lower() for tag in tag_string.split(','))
        tags = [TagObj.query.filter(TagObj.name == tag).first()
                or TagObj(tag)
                for tag in tag_set]

        for tag in tags:
            if tag not in getattr(self, rel):
                getattr(self, rel).append(tag)

class Genre(Base):
    """ Defines a Genre model. One Sheetmusic can have multiple Genre"""
    __tablename__ = 'genres'
    name = Column(Unicode(128))

    sheetmusic = relationship('Sheetmusic',
                              secondary=SheetmusicGenres,
                              back_populates='genre_tags')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Genre id={} name={}>".format(self.id, self.name)

    def __eq__(self, other):
        return bool(isinstance(other, type(self)) and self.name == other.name)


class Instrument(Base):
    """ Defines an Instrument model. One Sheetmusic can have multiple Instruments"""
    __tablename__ = 'instruments'
    name = Column(Unicode(128), unique=True)

    sheetmusic = relationship('Sheetmusic',
                              secondary=SheetmusicInstruments,
                              back_populates='instrumentation')
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Instrument id={} name={}>".format(self.id, self.name)

    def __eq__(self, other):
        """
        :param other: The other instrument object
        :return: boolean True if both objects are equal
        """
        return bool(isinstance(other, type(self)) and self.name == other.name)


