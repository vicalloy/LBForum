from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('attachments.views',
    url('^ajax_upload/$', 'ajax_upload', name='attachments_ajax_upload'),
)
