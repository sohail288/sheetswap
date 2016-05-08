from app.tests.test_base import AppTest, DBTest
from models import User, Item, Trade, Sheetmusic

class IntegratedTests(DBTest):

    def test_items_displayed_do_not_include_items_in_completed_trades(self):
        user1 = User(username='user1', email='user1@email.com', password='123456')
        user2 = User(username='user2', email='user2@email.com', password='123456')
        sheetmusic = Sheetmusic(composer='composer1', title='piece 2')
        item = Item(user=user1, sheetmusic_id=sheetmusic.id, condition='Clean')

        self.assertEqual(user1.items, user1.get_available_items())

        trade = Trade(item_to = item, user_to = user1, user_from = user2)
        self.assertEqual(user1.items, user1.get_available_items())

        trade.completed = True
        trade.rejected  = True
        self.assertEqual(user1.items, user1.get_available_items())

        trade.rejected = False
        self.assertNotEqual(user1.items, user1.get_available_items())








