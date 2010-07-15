from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.profile), name='account_index'),
    url(r'^signature/$', views.signature, name='signature'),
    (r'^', include('registration.backends.default.urls')),
)
