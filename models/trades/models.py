from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship, validates


from app.db import Base


class Trade(Base):

    """ A class the represents a trade """
    __tablename__ = 'trades'
    __table_args__ = (
        CheckConstraint('user_from_id != user_to_id'),
        CheckConstraint('item_from_id != item_to_id')
    )

    item_from_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item_to_id = Column(Integer, ForeignKey('items.id'))

    item_from = relationship('Item', back_populates='trades', foreign_keys=[item_from_id])
    item_to   = relationship('Item', back_populates='trades', foreign_keys=[item_to_id])

    user_from_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_to_id   = Column(Integer, ForeignKey('users.id'))

    completed = Column(Boolean, default=False)
    rejected  = Column(Boolean, default=False)

    trade_init_timestamp = Column(DateTime(), default=datetime.now)
    trade_fin_timestamp = Column(DateTime())


    @validates('item_from', 'item_to')
    def validate_items_are_from_owners(self, key, item):
        """

        :param key: the key that the signal will respond to, will be `item_from` or `item_to`
        :param item: the item that will be a part of the signal
        :return: the item if it belongs to the trader
        """
        if key == 'item_from':
            assert item.user.id == self.user_from_id
        elif key == 'item_to':
            assert item.user.id == self.user_to_id

        return item

    def __repr__(self):
        return "<Trade from_user={} to_user={} from_item={} to_item={}>".format(
            self.user_from_id,
            self.user_to_id,
            self.item_from_id,
            self.item_to_id
        )
