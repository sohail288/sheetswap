import unittest
from flask import url_for
from app.tests.test_base import AppTest


class AuthContextTests(AppTest):

    def login(self, email, password):
        """ Helper function """
        return self.client.post(url_for('auth.login'),
                                data=dict(
                                    email=email,
                                    password=password
                                ),
                                follow_redirects=True)

    def create_user(self, email, username, password):
        """ Create a temporary user """
        return self.client.post(url_for('auth.register'),
                                data=dict(
                                    email=email,
                                    username=username,
                                    password=password,
                                    check_password=password
                                ),
                                follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)

    def test_can_login_with_any_casing_of_word(self):
        email, username, password = 'swapper@swap.com', 'swapper', 'password'
        self.create_user(email, username, password)
        self.logout()

        rv = self.login(email, password)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome back', rv.data)
        self.logout()

        rv = self.login(email.upper(), password)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome back', rv.data)
        self.logout()

        # what about a space at the end?
        rv = self.login(email.upper() + ' ', password)

        self.assertNotIn(b'Welcome back', rv.data)
