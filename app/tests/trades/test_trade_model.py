import unittest
from models import Trade


class TradeModelTestCase(unittest.TestCase):

    def test_create_a_trade(self):
        t = Trade()
        self.assertIsNotNone(t)


