from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.utils.fields import password_field
from apps.utils.forms import AbstractFrom

from .base import AbstractRegistrationForm
from .models import PasswordReset, User
from .strings import FORMS


class RegistrationForm(AbstractRegistrationForm):
    title = "Register"
    helper = FormHelper()
    helper.add_input(Submit('login', 'login'))
    helper.render_required_fields = False
    helper.html5_required = True
    # helper.form_show_labels = False


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


