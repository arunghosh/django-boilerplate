from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _

from apps.utils.fields import password_field

from .base import RegistrationFormBase
from .models import PasswordReset, User
from .strings import FORMS


class RegistrationForm(RegistrationFormBase):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
    
    def _create_object(self, **kwargs):
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
  

class LoginForm(forms.Form):
    submit_button_name = 'Login'
    email = forms.EmailField(label=_("User Name/ Email"))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "********"}))

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        self.user = None
        self.error = "Invalid email and/or password"  
        super(LoginForm, self).__init__(*args, **kwargs)

    def authenticate(self, request):
        if self.is_valid():
            try:
                self.user = authenticate(
                    email=self.cleaned_data['email'], 
                    password=self.cleaned_data['password'])
                if self.user:
                    # self._check_confirm_and_login(request)
                    login(request, self.user)
            except Exception as e:
                print str(e)
        else:
            pass
        self.custom_errors.append(self.error)
        return self.user

    def _check_confirm_and_login(self, request):
        if self.user.is_confirmed:
            login(request, self.user)
            self.user.add_log(FORMS['user_logged'])
        else:
            self.error = "Email not verified"
            return self.user


