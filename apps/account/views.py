from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.conf import settings
from .forms import LoginForm



class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return self.home_view(request)
        form = LoginForm()
        return self._get_login_page(request, form);

    def post(self, request):
        form = LoginForm(request.POST)
        form.authenticate(request)
        if request.user.is_authenticated():
            return self.home_view(request)
        return self._get_login_page(request, form);

    def home_view(self, request):
        return redirect(request.GET.get('next', reverse("home")))

    def _get_login_page(self, request, form):
        return render(request, "login.html", {
          'form': form, 
          'fb_enabled': settings.FACEBOOK_LOGIN_ENABLED})
        

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse("home"))

