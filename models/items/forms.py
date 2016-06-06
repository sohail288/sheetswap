from wtforms import (Form,
                     StringField,
                     TextAreaField,
                     validators,
                     HiddenField,
                     FileField,
                     SelectField,
                     BooleanField,
                     )

from models.common.forms.forms import HiddenInteger

condition_choices = [
    ('new', 'New'),
    ('clean', 'Clean'),
    ('marked', 'Has markings'),
    ('missing', 'Is missing pages'),
    ('torn', 'Torn pages, but all there'),
    ('old', 'Oldish')
]


class CreateItemForm(Form):
    sheetmusic_id = HiddenInteger("sheetmusic_id")
    description = TextAreaField(validators=[validators.Length(max=255)])
    condition = SelectField('Condition', choices=condition_choices)
    images = FileField('Sheetmusic Images', render_kw={'multiple': True})


class EditItemForm(Form):
    description = TextAreaField(validators=[validators.Length(max=256)])
    images = FileField('Sheetmusic Images', render_kw={'multiple': True})
    condition = SelectField('Condition', choices=condition_choices)
    available = BooleanField('Available?')
