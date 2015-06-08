from abc import abstractmethod

from django.db import transaction
from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.utils.fields import password_field
from apps.utils.forms import AbstractFrom

from .models import PasswordReset, User
from .strings import FORMS


class AbstractRegistrationForm(AbstractFrom):

    title = "Register"

    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    helper = FormHelper()
    helper.add_input(Submit('Register', 'Register'))
    helper.render_required_fields = False
    helper.html5_required = True

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


class PasswordResetForm(forms.Form):
    submit_button_name = 'Reset Password'
    password = password_field
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "********"}))
    key = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        super(PasswordResetForm, self).__init__(*args, **kwargs)
 
    def clean_confirm_password(self):
        cleaned_data = super(PasswordResetForm, self).clean() 
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password != confirm:
            raise forms.ValidationError('Confirm password not matching.')
        return confirm

    def save(self):
        if self.is_valid():
            reset = PasswordReset.objects.get(key=self.cleaned_data['key'])
            if reset.is_expired:
                self.custom_errors.append('Token expired')
                return False
            else:
                user = reset.user
                user.set_password(self.cleaned_data['password'])
                user.save()
        return True      
  

class LoginForm(AbstractFrom):
    email = forms.EmailField(label=_("User Name/ Email"))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "********"}))
    
    error = 'Invalid email and/or password'
    button_name = 'Login'

    def authenticate(self, request):
        self.context['request'] = request
        if self.is_valid():
            self.user = authenticate(
                email=self.cleaned_data.get('email', None), 
                password=self.cleaned_data.get('password', None))
            if self.user:
                # self._check_confirm_and_login(request)
                login(request, self.user)
            else:
                self.add_error(self.error)
        return self.user

    def _check_confirm_and_login(self):
        if self.user.is_confirmed:
            login(self.context['request'], self.user)
            self.user.add_log(FORMS['user_logged'])
        else:
            self.add_error("Email not verified")
            return self.user


