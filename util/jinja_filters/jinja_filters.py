"""
    This module contains filters used by the main program, the filters are registered in
    the run.py file
"""

def pluralize(word, quantity, plural_form='s'):
    if quantity == 1:
        return word
    else:
        if plural_form == 's':
            if not word.endswith('y'):
                return word + plural_form
        else:
            return plural_form

