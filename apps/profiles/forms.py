from abc import abstractmethod

from django.db import transaction
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.utils.fields import password_field
from apps.utils.forms import AbstractFrom

from apps.account.models import User


class AbstractRegistrationForm(AbstractFrom):

    title = 'Register'
    button_name = 'Register'

    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    @abstractmethod
    def create_object(self, **kwargs):
        ''' 
        You can overrride object creation in the firn save method
        ex: CustomUser.objects.register(**kwargs)
        '''
        # profile.register()
        pass

    def clean_email_confirm(self):
        ''' Check if email and confirm email are the same
        '''
        cleaned_data = super(AbstractRegistrationForm, self).clean() 
        email = cleaned_data.get('email')
        confirm = cleaned_data.get('email_confirm')
        if email != confirm:
            raise forms.ValidationError('Confirm email not matching.')
        return confirm
  
    @transaction.atomic
    def save(self):
        try:
            self.cleaned_data.pop('email_confirm')
            return self.create_object(**self.cleaned_data)
        except ValueError as e:
            self.add_error(str(e))
        except Exception as e:
            #TODO log
            print e
            self.add_error("Failed to register user.")
        return


class RegistrationForm(AbstractRegistrationForm):

    def create_object(self, **kwargs):
        return User.objects.create_user(**kwargs)
