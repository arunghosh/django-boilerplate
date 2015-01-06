from django.conf.urls import patterns, url
from .views import register_and_login 

urlpatterns = patterns('',
    url(r'login/(?P<access_token>[-\w\d]+)$', register_and_login),
)

