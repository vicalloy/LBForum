from django.conf.urls.defaults import *
from lbforum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='lbforum_index'),                       
    url(r'^forum/(?P<forum_slug>\w+)/$', views.forum, name='lbforum_forum'),
    url('^topic/(?P<topic_id>\d+)/$', views.topic, name='lbforum_topic'),    
)
