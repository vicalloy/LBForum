from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('attachments.views',
    url('^ajax_upload/$', 'ajax_upload', name='attachments_ajax_upload'),
    url('^ajax_delete/$', 'ajax_delete', name='attachments_ajax_delete'),
    url('^ajax_change_descn/$', 'ajax_change_descn', name='attachments_ajax_change_descn'),
)
