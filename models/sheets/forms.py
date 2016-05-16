"""
Generates HTML forms via WTForms for sheets
"""

from wtforms import (Form,
                     BooleanField,
                     StringField,
                     IntegerField,
                     FileField,
                     validators)
from wtforms.widgets import HiddenInput

TS_REGEXP = r'(^\s*$|common|half|waltz|march|alla\s*?breve)'
TS_REGEXP += r'|([1-9][0-9]?\s*?[ \/]\s*?[1-9][0-9]?)'


class HiddenInteger(IntegerField):
    widget = HiddenInput()


class SheetMusicForm(Form):
    title = StringField(u'Title', [validators.DataRequired()])
    composer = StringField(u'Composer', [validators.Length(max=255)])
    instrumentation = StringField(u'Instrumentation', [validators.Length(max=255)])
    arranged_by = StringField(u'Arranged by')
    genre = StringField(u'Genre', [validators.Length(max=255)])
    time_signature = StringField(u'Time Signature', [validators.Regexp(regex=TS_REGEXP)])
    cover = FileField(u'Cover Picture',  [validators.Optional(), validators.regexp(u'^[^\\/]+\.(jpg|png)$')])
    creating_item = HiddenInteger('creating_item')
