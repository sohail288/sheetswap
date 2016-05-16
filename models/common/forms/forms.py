from wtforms import IntegerField
from wtforms.widgets import HiddenInput


class HiddenInteger(IntegerField):

    widget = HiddenInput()
