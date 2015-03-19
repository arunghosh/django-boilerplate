from django.conf.urls import patterns, url
from .views import LoginView, LogoutView, profile, confirm_email, \
    SendConfirmEmail, SendPasswordResetMail, PasswordResetView, RegisterView

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^password/reset/(?P<id>[0-9]*)/(?P<key>[-\w\d]+)$', PasswordResetView.as_view(), name="password_reset"),
    url(r'^password/send-reset/$', SendPasswordResetMail.as_view(), name="send_password_reset"),
    url(r'^email/send-verify/$', SendConfirmEmail.as_view(), name="resend_email_confirm"),
    url(r'^email/confirm/(?P<id>[0-9]*)/(?P<key>[-\w\d]+)$', confirm_email, name="email_confirm"),
    url(r'^profile/$', profile, name='profile'),
)
