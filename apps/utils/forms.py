from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AbstractFrom(forms.Form):
    button_name = 'Submit'

    def __init__(self, *args, **kwargs):
        super(AbstractFrom, self).__init__(*args, **kwargs)
        self.context = {}
        self.helper = self.get_crispy_helper()

    def get_crispy_helper(self):
        helper= FormHelper()
        helper.add_input(Submit(self.button_name, self.button_name))
        helper.render_required_fields = False
        helper.html5_required = True
        return helper

    def add_common_error(self, msg):
        self.errors['__all__'] = self.errors.get('__all__', [])
        self.errors['__all__'].append(msg)
