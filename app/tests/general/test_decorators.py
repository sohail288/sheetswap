import unittest
from unittest import mock
from collections import namedtuple

from flask import url_for
from app.tests.test_base import AppTest
from app.decorators import user_is_part_of_trade, user_is_logged_in, user_passes_test


@mock.patch('app.decorators.url_for')
@mock.patch('app.decorators.redirect')
@mock.patch('app.decorators.flash')
@mock.patch('app.decorators.g')
class DecoratorTests(unittest.TestCase):

    User = namedtuple('User', 'id trade_ids')
    Trade = namedtuple('Trade', 'id user_from_id user_to_id')


    def test_user_is_part_of_trade__correctly_wraps_function(self, g, flash, redirect, url_for):

        @user_is_part_of_trade()
        def a_controller(request):
            return request

        self.assertEqual(a_controller.__name__, 'a_controller')

    def test_user_is_part_of_trade__prevents_unauthorized_access(self, g, flash, redirect, url_for):
        user = self.User(3, [2,3,4])
        g.configure_mock(user=user)

        @user_is_part_of_trade(on_error=404)
        def a_controller(trade_id):
            return 'secret info'

        a_controller(1)
        flash.assert_called_with('You are not a part of that trade', 'error')
        url_for.assert_called_with('main.dashboard')
        redirect.assert_called_with(url_for('main.dashboard'))

    def test_user_is_part_of_trade__allows_authorized_access(self, g, flash, redirect, url_for):
        user = self.User(1, [1])
        g.configure_mock(user=user)

        @user_is_part_of_trade(on_error=404)
        def a_controller(trade_id):
            return 'secret info'

        self.assertEqual(a_controller(1), 'secret info')

    def test_user_is_logged_in__allows_logged_in_behavior(self, g, flash, redirect, url_for):
        user = self.User(1, [1])
        g.configure_mock(user=user)

        @user_is_logged_in
        def a_controller():
            return 'secret info'

        rv = a_controller()
        self.assertEqual(rv, 'secret info')

        flash.assert_not_called()
        redirect.assert_not_called()
        url_for.assert_not_called()

    # request is added to the arguments list first.  Then it is followed by the class decorations
    @mock.patch('app.decorators.request')
    def test_user_is_logged_in__prevents_unauthorized_access(self, request, g, flash, redirect, url_for):
        g.configure_mock(user=None)

        @user_is_logged_in
        def a_controller():
            return 'secret info'

        rv = a_controller()

        flash.assert_called_with('Must be logged in to access that')
        redirect.assert_called_with(url_for('auth.login'))

        flash.reset_mock()
        redirect.reset_mock()

        request.configure(next='trades/2')
        a_controller()

        url_for.assert_called_with('auth.login', next=request.path)

    @mock.patch('app.decorators.request')
    @mock.patch('app.decorators.abort')
    def test_user_passes_a_test_to_do_something(self, abort, request, g, flash, redirect, url_for):
        g.configure_mock(user=self.User(1, []))

        def prevent_user_with_id_one(): return False if g.user.id == 1 else True

        @user_passes_test(test_func=prevent_user_with_id_one)
        def a_controller():
            return 'secret info'

        rv = a_controller()
        self.assertTrue(abort.called)
        abort.reset_mock()

        g.configure_mock(user=self.User(2, []))

        rv = a_controller()
        self.assertFalse(abort.called)
        self.assertEqual(rv, 'secret info')




class DecoratorContextTests(AppTest):

    def test_user_is_logged_in__redirects_to_login_page(self):
        response = self.client.get(url_for('trades.main', trade_id=1),
                                   follow_redirects=True)

        self.assertIn('Must be logged in to access that', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_user_is_part_of_trade__redirects_to_dashboard(self):
        response = self.client.post(url_for('auth.login'),
                         data=dict(email='mary@email.com', password='password'),
                         follow_redirects=True,
                         )

        self.assertIn('Welcome', response.get_data(as_text=True))

        response = self.client.get(url_for('trades.main', trade_id=10000), follow_redirects=True)

        self.assertIn('not a part', response.get_data(as_text=True))

    def test_user_is_logged_in__permits_legal_login(self):
        response = self.client.post(url_for('auth.login'),
                                    data=dict(email='mary@email.com', password='password'),
                                    follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.get_data(as_text=True))




