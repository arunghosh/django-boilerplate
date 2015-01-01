from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email Address"))
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def authenticate(self, request):
        if self.is_valid():
            try:
                #email = self.
                #user = User.objects.get(email=self.cleaned_data['email'],
                                            #type__in=(UT_PLAYER, UT_FACULTY))
                self.user = authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
                if self.user:
                    login(request, self.user)
            except:
                pass

            if not self.user:
                self.custom_errors.append("Invalid user name or password")
        return self.user


