from sqlalchemy.exc import IntegrityError

from app.tests.test_base import DBTest
from models import Trade, User, Item

class TradeModelPersistenceTests(DBTest):

    def test_do_not_allow_user_to_trade_with_self(self):
        user_from = User('abe@email.com', 'abe', '1234')
        user_to = User('lincoln@email.com', 'lincoln', '4321')
        trade = Trade(user_from_id=user_from.id, user_to_id=user_from.id)

        self.db.add(trade)

        with self.assertRaises(IntegrityError):
            self.db.commit()

    def test_items_must_belong_to_their_respective_owners(self):
        user_from = User('abe@email.com', 'abe', '1234')
        user_to = User('lincoln@email.com', 'lincoln', '4321')
        item_from = Item(user=user_from)
        item_to   = Item(user=user_to)
        self.db.add_all([user_from, user_to, item_from, item_to])
        self.db.commit()

        # from to swap
        with self.assertRaises(AssertionError):
            trade = Trade( user_from_id=user_from.id,  user_to_id=user_to.id, item_from=item_to, item_to=item_from)

        # to from swap
        with self.assertRaises(AssertionError):
            trade = Trade(user_from_id=user_to.id, user_to_id=user_from.id, item_to=item_from, item_from=item_from)



