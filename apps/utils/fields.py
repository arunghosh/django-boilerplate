from django import forms
from django.db import models
import apps.utils.validators as v


password_field = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "********"}), help_text=v.password.help_text, validators=v.password.validators)


class CSVCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = 'Enter mutiple values separated by comma' 
        super(CSVCharField, self).__init__(*args, **kwargs)


class CSVTextField(models.TextField):

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = 'Enter mutiple values separated by comma' 
        super(CSVTextField, self).__init__(*args, **kwargs)
