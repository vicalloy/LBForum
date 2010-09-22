from django.conf.urls.defaults import patterns, url

from djangohelper.helper import flash_login_required, ajax_login_required

import views
urlpatterns = patterns('',
    url('^ajax_upload/$', views.ajax_upload, name='attachments_ajax_upload'),
    url('^ajax_delete/$', views.ajax_delete, name='attachments_ajax_delete'),
    url('^ajax_change_descn/$', views.ajax_change_descn, name='attachments_ajax_change_descn'),
    url('^uploadify/$', views.uploadify, name='attachments_uploadify'),
)
