# test the jinja filters

import unittest
from util.jinja_filters.jinja_filters import pluralize


class JinjaTests(unittest.TestCase):

    def test_pluralizes_a_word(self):
        word = 'puppy'
        correct_plural = 'puppies'

        plural_word = pluralize(word, 0, 'puppies')
        nonplural_word = pluralize(word, 1)

        self.assertEqual(nonplural_word, word)
        self.assertEqual(correct_plural, plural_word)


