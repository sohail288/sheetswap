import unittest
from app.tests.test_base import AppTest
from models import User, Address


class UserModelTestCase(unittest.TestCase):

    def test_create_a_user(self):
        u = User()
        self.assertIsNotNone(u)

    def test_user_email_must_contain_at_symbol(self):
        # it must contain an email symbol
        with self.assertRaises(AssertionError):
            u = User(email='abracadabra')

        # it has to have an email symbol and something after the at symbol
        with self.assertRaises(AssertionError):
            u = User(email='abracadabra@')

        u = User(email='abracadabra@something.com')

        self.assertIsNotNone(u.email)



    def test_user_password_is_hashed(self):
        password = 'jsalkdfjaskfkjfs_?a'

        u = User(password=password)

        self.assertNotEqual(password, u.password_hash)

    def test_cant_access_password_attribute(self):
        password = 'abcdef'

        u = User(password=password)

        with self.assertRaises(AttributeError):
            u.password

    def test_can_unhash_password_given_correct_password(self):
        password = 'aintthisatreat'

        u = User(password=password)
        verified_password = u.verify_password(password)
        unverified_password = u.verify_password('nope')

        self.assertTrue(verified_password)
        self.assertFalse(unverified_password)

    def test_is_it_salting_correctly(self):
        u = User(password='one')
        u2 = User(password='two')

        self.assertNotEqual(u.password_hash, u2.password_hash)

class AddressModelTestcase(unittest.TestCase):

    def test_create_an_address(self):
        a = Address()

        self.assertIsNotNone(a)

    def test_attach_an_address(self):
        a = Address()
        u = User()

        u.addresses.append(a)

        self.assertEqual(len(u.addresses), 1)


