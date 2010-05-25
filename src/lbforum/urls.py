from django.conf.urls.defaults import *
from lbforum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='lbforum_index'),
    url(r'^forum/(?P<forum_slug>\w+)/$', views.forum, name='lbforum_forum'),
    url('^topic/(?P<topic_id>\d+)/$', views.topic, name='lbforum_topic'),    
    url('^topic/new/(?P<forum_id>\d+)/$', views.new_post, name='lbforum_new_topic'),
    url('^reply/new/(?P<topic_id>\d+)/$', views.new_post, name='lbforum_new_replay'),    
    url('^post/(?P<post_id>\d+)/$', views.post, name='lbforum_post'),    
    url('^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='lbforum_post_edit'),    
    url('^user/(?P<user_id>\d+)/topics/$', views.user_topics, name='lbforum_user_topics'),    
    url('^user/(?P<user_id>\d+)/posts/$', views.user_posts, name='lbforum_user_posts'),    

    url('^markitup_preview/$', views.markitup_preview, name='markitup_preview'),    
)
