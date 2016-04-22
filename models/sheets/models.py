
"""
    Models for sheet music
"""


from sqlalchemy import Table, Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.models import Base


SheetmusicGenres = Table('sheetmusic_genres', Base.metadata,
                         Column('sheetmusic_id', Integer, ForeignKey('sheetmusic.id')),
                         Column('genre_id', Integer, ForeignKey('genre.id'))
)

SheetmusicInstruments = Table('sheetmusic_instruments', Base.metadata,
                              Column('sheetmusic_id', Integer, ForeignKey('sheetmusic.id')),
                              Column('instrument_id', Integer, ForeignKey('instrument.id'))
)

class Sheetmusic(Base):
    __tablename__ = "sheetmusic"

    title = Column(Unicode(255), unique=True)
    cover = Column(Unicode(255), unique=True)
    composer = Column(Unicode(255))
    arranged_by = Column(Unicode(255))

    time_signature = Column(Unicode(64))

    genre_tags =  relationship('Genre',
                               secondary=SheetmusicGenres)
    instrumentation = relationship('Instrument',
                                   secondary=SheetmusicInstruments)

    def __repr__(self):
        return '<Sheetmusic id={} title={} composer={}>'.format(
            self.id,
            self.title,
            self.composer
        )

class Genre(Base):
    """ Defines a Genre model. One Sheetmusic can have multiple Genre"""
    __tablename__ = 'genre'
    name = Column(Unicode(128))

    def __repr__(self):
        return "<Genre id={} name={}>".format(self.id, self.name)


class Instrument(Base):
    """ Defines an Instrument model. One Sheetmusic can have multiple Instruments"""
    __tablename__ = 'instrument'
    name = Column(Unicode(128))

    def __repr__(self):
        return "<Instrument id={} name={}>".format(self.id, self.name)


