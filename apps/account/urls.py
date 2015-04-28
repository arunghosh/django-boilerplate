from django.conf.urls import patterns, url
from .views import LoginView, LogoutView, email_confirm_view, \
    SendConfirmEmailView, SendPasswordResetMailView, PasswordResetView, RegisterView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^password/reset/(?P<id>[0-9]*)/(?P<key>[-\w\d]+)$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/send-reset/$', SendPasswordResetMailView.as_view(), name='send_password_reset'),
    url(r'^email/send-verify/$', SendConfirmEmailView.as_view(), name='resend_email_confirm'),
    url(r'^email/confirm/(?P<id>[0-9]*)/(?P<key>[-\w\d]+)$', email_confirm_view, name='email_confirm'),
)
