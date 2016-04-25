from sqlalchemy import (Column,
                        Unicode,
                        UnicodeText,
                        Boolean,
                        Integer,
                        DateTime,
                        ForeignKey)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base

#from models.sheets import Sheetmusic


class Item(Base):

    """
        Represents an owned instance of a tradeable object, in this case, Sheetmusic
    """
    __tablename__ = 'items'
    sheetmusic_id = Column(Integer(), ForeignKey('sheetmusic.id'))
    sheetmusic = relationship('Sheetmusic', back_populates='items')

    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship('User', back_populates='items')

    available = Column(Boolean(), default=True)

    images = relationship('ItemImage', back_populates='item')

    added_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    description = Column(Unicode(256))
    condition = Column(Unicode(32))


    def __repr__(self):
        return "<Item id = {} sheetmusic={} user={} condition={}>".format(self.id,
                                                                  self.sheetmusic.title,
                                                                  self.user.username,
                                                                  self.condition)


class ItemImage(Base):
    __tablename__ = 'item_images'

    item_id =  Column(Integer, ForeignKey('items.id'))
    item = relationship('Item', back_populates='images')
    timestamp = Column(DateTime(), default=datetime.now)
    image = Column(Unicode(256), nullable=False)

    def __repr__(self):
        return "<ItemImage item_id={} timestamp={}>".format(self.item_id, self.timestamp)

