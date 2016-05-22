from app.tests.test_base import DBTest
from models import User, Address


class UserModelPersistenceTests(DBTest):

    def test_save_and_retrieve_user_model(self):
        u = User(email='joe@email.com', username='joe', password='123456')
        self.db.add(u)

        self.assertGreater(len(self.db.new), 0)

        self.db.commit()

        self.assertEqual(len(self.db.new), 0)

        u_query = self.db.query(User).first()

        self.assertEqual(u_query, u)
        self.assertEqual(u.id, 1)

    def test_can_the_db_deal_with_casing(self):
        auth_info = dict(email='JOE@email.com', username='joe', password='123456')
        u = User(**auth_info)
        self.db.add(u)
        self.db.commit()

        u_query = self.db.query(User).filter_by(email=auth_info['email'].lower()).one_or_none()

        self.assertIsNotNone(u_query)

    def test_check_backreferences(self):
        u = User(email='joe@email.com', username='joe', password='123456')
        a = Address(street_address='123 abbey ln',
                    city='somecity',
                    state='CA',
                    postal_code='95240',
                    country='USA')
        u.addresses.append(a)

        self.db.add(u)

        self.assertEqual(len(self.db.new), 2)

        self.db.commit()

        self.assertEqual(u.addresses[0], a)
        self.assertEqual(a.user, u)

