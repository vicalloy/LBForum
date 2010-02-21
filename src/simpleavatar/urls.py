from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('simpleavatar.views',
    url('^change/$', 'change', name='avatar_change'),
)
