"""
    This module contains filters used by the main program, the filters are registered in
    the run.py file
"""

import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

def pluralize(word, quantity, plural_form='s'):
    if quantity == 1:
        return word
    else:
        if plural_form == 's':
            if not word.endswith('y'):
                return word + plural_form
        else:
            return plural_form


word_numbers = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven']

def time_ago(date, today=datetime.datetime.now()):

    if not isinstance(today, datetime.datetime):
        today = parse(today)
    if not isinstance(date, datetime.datetime):
        date_obj = parse(date)

    time_delta = relativedelta(today, date_obj)

    if not any([time_delta.months, time_delta.days, time_delta.weeks, time_delta.years]):
        date_since_string = 'today'
    elif time_delta.years and time_delta.years != 1:
        date_since_string = '{} years'.format(word_numbers[time_delta.years])
    elif time_delta.years:
        date_since_string = 'one year'
    elif time_delta.months and time_delta.months != 1:
        date_since_string = '{} months'.format(word_numbers[time_delta.months])
    elif time_delta.months == 1:
        date_since_string = 'one month'
    elif time_delta.weeks and time_delta.weeks != 1:
        date_since_string = '{} weeks'.format(word_numbers[time_delta.weeks])
    elif time_delta.weeks:
        date_since_string = 'a week'
    elif time_delta.days and time_delta.days != 1:
        date_since_string = '{} days'.format(word_numbers[time_delta.days])
    else:
        date_since_string = 'yesterday'

    date_string = 'Added ' + date_since_string
    date_string += ' ago' if not date_string.endswith('day') else ''
    return date_string


