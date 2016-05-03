import unittest
from unittest import mock
from collections import namedtuple
from app.tests.test_base import AppTest
from app.decorators import user_is_part_of_trade
from werkzeug.exceptions import BadRequest


@mock.patch('app.decorators.g')
class DecoratorTests(unittest.TestCase):

    User = namedtuple('User', 'id trades')
    Trade = namedtuple('Trade', 'id user_from_id user_to_id')


    def test_user_is_part_of_trade__correctly_wraps_function(self, g):

        @user_is_part_of_trade()
        def a_controller(request):
            return request

        self.assertEqual(a_controller.__name__, 'a_controller')

    def test_user_is_part_of_trade__prevents_unauthorized_access(self, g):
        user = self.User(3, [2,3,4])
        trade = self.Trade(1,1,2)
        g.configure_mock(user=user)

        @user_is_part_of_trade(on_error=404)
        def a_controller(trade_id):
            return 'secret info'

        with self.assertRaises(BadRequest):
            a_controller(1)

    def test_user_is_part_of_trade__allows_authorized_access(self, g):
        user = self.User(1, [1])
        trade = self.Trade(1,1,2)
        print(g)
        g.configure_mock(user=user)

        @user_is_part_of_trade(on_error=404)
        def a_controller(trade_id):
            return 'secret info'

        self.assertEqual(a_controller(1), 'secret info')



