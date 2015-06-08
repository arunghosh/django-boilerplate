from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AbstractFrom(forms.Form):
    button_name = 'Submit'

    def __init__(self, *args, **kwargs):
        super(AbstractFrom, self).__init__(*args, **kwargs)
        self.context = {}
        self.helper= FormHelper()
        self.helper.add_input(Submit(self.button_name, self.button_name))

    def add_error(self, msg):
        self.errors['__all__'] = self.errors.get('__all__', [])
        self.errors['__all__'].append(msg)
