from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib import messages

from apps.utils.views import handle_success, AbstractFormView
from .strings import PASSWORD
from .forms import LoginForm, PasswordResetForm
from .models import EmailAddress, EmailConfirm, PasswordReset, User


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return self.home_view(request)
        self.form = LoginForm()
        return self._get_login_page();

    def post(self, request):
        self.form = LoginForm(request.POST)
        self.form.authenticate(request)
        if request.user.is_authenticated():
            return self.home_view()
        return self._get_login_page();

    def home_view(self):
        return redirect(self.request.GET.get('next', reverse("home")))

    def _get_login_page(self):
        return render(self.request, 'account/login.html', { 'form': self.form })
        

def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


def email_confirm_view(request, id, key):
    try:
        email_confirm = EmailConfirm.objects.get(key=key)
        email_confirm.confirm()
        return handle_success(
            request, 'Thank you for confirming your email address. Login to continue.', reverse('login')) 
    except EmailConfirm.DoesNotExist:
        messages.info(request, 'Failed to confirm your email. Request another confirmation token')
        return redirect(reverse('resend_email_confirm'))


class SendConfirmEmailView(TemplateView):
    template = 'account/email_confirm_resend.html' 

    def post(self, request):
        email = request.POST.get('email', None)
        if EmailAddress.objects.send_confirm(email):
            return handle_success(request, 'Verification mail is sent to your Inbox. If not found in Inbox check junk mail.')
        messages.info(request, 'Failed to send confirm mail. Please check your email address')
        return render(request, self.template, {'email': email})
      

class SendPasswordResetMailView(TemplateView):
    template_name = 'account/password/reset_send.html' 

    def post(self, request):
        try:
            email = request.POST.get('email', None)
            PasswordReset.create_from_email(email).send()
            return handle_success(request, PASSWORD['mail_send'])
        except User.DoesNotExist:
            messages.info(request, 'The email is not registered. Please check your email address')
            return render(request, self.template, {'email': email})
      

class PasswordResetView(AbstractFormView):
    template_name = 'account/password/reset.html'
    form_class = PasswordResetForm
    success_message = 'Password Successfully Updated'
    success_url = reverse_lazy('login')

    def get_initial(self):
        return {'key': self.kwargs}
