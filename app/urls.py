from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('account.urls')),
    url(r'^fb/', include('fb.urls')),
    url(r'^thankyou/$', TemplateView.as_view(template_name="thankyou.html"), name="thankyou"),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="home"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
          (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
          'document_root': settings.STATIC_ROOT}))

urlpatterns += patterns('',
)
