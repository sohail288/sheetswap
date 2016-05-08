# test the jinja filters

import unittest
from util.jinja_filters.jinja_filters import pluralize, time_ago


class JinjaTests(unittest.TestCase):

    def test_pluralizes_a_word(self):
        word = 'puppy'
        correct_plural = 'puppies'

        plural_word = pluralize(word, 0, 'puppies')
        nonplural_word = pluralize(word, 1)

        self.assertEqual(nonplural_word, word)
        self.assertEqual(correct_plural, plural_word)

    def test_get_time_ago(self):
        ref_date = '05/01/2016'
        two_months_later = '07/01/2016'
        week_later = '05/08/2016'
        two_days_later = '05/03/2016'
        day_later = '05/02/2016'
        today = ref_date
        three_weeks_later = '05/27/2016'
        five_weeks_later  = '06/04/2016'
        three_years_later = '05/01/2019'

        self.assertEqual(time_ago(ref_date, two_months_later),
                         'Added two months ago')
        self.assertEqual(time_ago( ref_date, week_later),
                                  'Added a week ago')
        self.assertEqual(time_ago(ref_date, day_later),
                         'Added yesterday')
        self.assertEqual(time_ago(ref_date, two_days_later),
                         'Added two days ago')
        self.assertEqual(time_ago(ref_date, today),
                         'Added today')
        self.assertEqual(time_ago(ref_date, three_weeks_later),
                         'Added three weeks ago')
        self.assertEqual(time_ago(ref_date, five_weeks_later),
                         'Added one month ago')
        self.assertEqual(time_ago(ref_date, three_years_later),
                         'Added three years ago')



