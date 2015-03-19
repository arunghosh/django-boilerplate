from django.http import Http404
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse, reverse_lazy

from django.conf import settings
from django.contrib import messages

from apps.utils.views import handle_success, FormView
from .strings import PASSWORD
from .forms import LoginForm, PasswordResetForm, RegistrationForm
from .models import EmailAddress, EmailConfirm, PasswordReset, User


class RegisterView(FormView):
    template = "form_edit.html"
    form = RegistrationForm
    success = "Thanks for resgistering with us. Complete the regisration process by responding to the verfication email."
    title = "User Registration"
    submit_name = "Register"


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
          'submit_name': 'Login',
          'fb_enabled': settings.FACEBOOK_LOGIN_ENABLED})
        

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse("home"))


def profile(request):
    if request.user.is_patient:
        return redirect(reverse('patient_profile_edit', kwargs={'section': 'biodata'} ))
    if request.user.is_doctor:
        return redirect(reverse('doctor_profile_edit', kwargs={'section': 'personal'}))
    raise Http404()
    

def confirm_email(request, id, key):
    try:
        email_confirm = EmailConfirm.objects.get(key=key)
        email_confirm.confirm()
        return handle_success(
            request, 
            'Thank you for confirming your email address. Login to continue.', 
            reverse('login') + '?username=' + email_confirm.email_address.user.username) 
    except EmailConfirm.DoesNotExist:
        messages.info(request, 'Failed to confirm your email. Request another confirmation token')
        return redirect(reverse('resend_email_confirm'))


class SendConfirmEmail(View):
    template = 'resend.html' 

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        email = request.POST.get('email', None)
        if EmailAddress.objects.send_confirm(email):
            return handle_success(request, 'Verification mail is sent to your Inbox. If not found in Inbox check junk mail.')
        messages.info(request, 'Failed to send confirm mail. Please check your email address')
        return render(request, self.template, {'email': email})
      

class SendPasswordResetMail(View):
    template = 'password/reset_send.html' 

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        try:
            email = request.POST.get('email', None)
            PasswordReset.create_from_email(email).send()
            return handle_success(request, PASSWORD['mail_send'])
        except User.DoesNotExist:
            messages.info(request, 'The email is not registered. Please check your email address')
            return render(request, self.template, {'email': email})
      

class PasswordResetView(FormView):
    template = 'password/reset.html'
    form = PasswordResetForm
    submit_name = 'Update Password'
    success_url = reverse_lazy('login')

    def get(self, request, id, key):
        return super(PasswordResetView, self).get(request, initial={'key': key})

    def post(self, request, id, key):
        return super(PasswordResetView, self).post(request)
