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
from models.trades import Trade

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

    _images = relationship('ItemImage', back_populates='item')

    added_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    description = Column(Unicode(256))
    condition = Column(Unicode(32))

    trades = relationship('Trade',
                          primaryjoin="or_(Trade.item_from_id == Item.id, "
                                      "Trade.item_to_id == Item.id)")

    @property
    def images(self):
        return [item_image.image for item_image in self._images]

    @images.setter
    def images(self, value):
        """
        :param value: the image to be set
        :return: None, you cannot set the item this way
        """
        pass

    def __repr__(self):
        return "<Item id = {} sheetmusic={} user={} condition={}>".format(self.id,
                                                                  self.sheetmusic.title,
                                                                  self.user.username,
                                                                  self.condition)


class ItemImage(Base):
    __tablename__ = 'item_images'

    item_id =  Column(Integer, ForeignKey('items.id'))
    item = relationship('Item', back_populates='_images')
    timestamp = Column(DateTime(), default=datetime.now)
    image = Column(Unicode(256), nullable=False, unique=True)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return "<ItemImage item_id={} timestamp={}>".format(self.item_id, self.timestamp)

