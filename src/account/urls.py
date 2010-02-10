from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.profile, name='account_index'),
)
