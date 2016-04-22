"""
Generates HTML forms via WTForms for sheets
"""

from wtforms import Form, BooleanField, StringField, IntegerField, FileField, validators

TS_REGEXP = r'(common|half|waltz|march|alla\s*?breve)'
TS_REGEXP += r'|([1-9][0-9]?\s*?[ \/]\s*?[1-9][0-9]?)'

class SheetMusicForm(Form):
    title = StringField(u'Title', [validators.DataRequired()])
    composer = StringField(u'Composer', [validators.Length(min=1)])
    instrumentation = StringField(u'Instrumentation', [validators.Length(min=1)])
    genre = StringField(u'Instrumentation', [validators.Length(min=1)])
    time_signature = StringField(u'Instrumentation', [validators.Regexp(regex=TS_REGEXP)])
    cover = FileField(u'Cover Picture', [validators.regexp(u'^[^/\\]\.jpg$')])

