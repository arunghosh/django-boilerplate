from abc import ABCMeta, abstractmethod
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django import forms
import apps.utils.validators as v
from .fields import password_field


class RegistrationFormBase(forms.Form):

    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), help_text=v.password.help_text, validators=v.password.validators)
    # mobile = forms.CharField(validators=v.mobile.validators)

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        super(RegistrationFormBase, self).__init__(*args, **kwargs)

    @abstractmethod
    def _create_object(self, **kwargs):
        pass

    def clean_email_confirm(self):
        cleaned_data = super(RegistrationFormBase, self).clean() 
        email = cleaned_data.get('email')
        confirm = cleaned_data.get('email_confirm')
        if email != confirm:
            raise forms.ValidationError('Confirm email not matching.')
        return confirm
  
    @transaction.atomic
    def save(self):
        if self.is_valid():
            try:
                return self._create_object(
                    email=self.cleaned_data['email'],
                    password=self.cleaned_data['password'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name']),
                    # mobile=self.cleaned_data['mobile'],)
            except ValueError as e:
                self.custom_errors.append(str(e))
            except Exception as e:
                #TODO log
                print e
                self.custom_errors.append("Failed to register user.")
            return

