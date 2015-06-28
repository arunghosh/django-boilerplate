from django.conf.urls import patterns, url, include
# from .views import ProfileViewSet
from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()
# router.register('profiles', ProfileViewSet, base_name='profiles')

urlpatterns = patterns('',
    url(r'^profile/register/$', views.RegisterView.as_view(), name='register'),
    url(r'^api/', include(router.urls)),
)
