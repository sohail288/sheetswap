from wtforms import Form, StringField, TextAreaField, validators, HiddenField


class CreateItemForm(Form):
    sheetmusic_id = HiddenField()

    condition   = StringField
    description = TextAreaField()


