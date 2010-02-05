from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from registration.views import register

admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^accounts/register/$',
        register,
        { 'backend': 'lbregistration.backends.simple.SimpleBackend' },
        name='registration_register'),    
    (r'^accounts/avatar/', include('avatar.urls')),#profile
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^', include('lbforum.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
