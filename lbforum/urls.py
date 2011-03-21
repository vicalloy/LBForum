from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from lbforum import views, accountviews 

urlpatterns = patterns('',
    url(r'^$', views.index, name='lbforum_index'),
    url(r'^forum/(?P<forum_slug>\w+)/$', views.forum, name='lbforum_forum'),
    url(r'^forum/(?P<forum_slug>\w+)/(?P<topic_type>\w+)/$', views.forum, name='lbforum_forum_ext'),
    url(r'^forum/(?P<forum_slug>\w+)/(?P<topic_type>\w+)/(?P<topic_type2>\w+)/$', 
        views.forum, name='lbforum_forum_ext2'),
    url('^topic/(?P<topic_id>\d+)/$', views.topic, name='lbforum_topic'),    
    url('^topic/new/(?P<forum_id>\d+)/$', views.new_post, name='lbforum_new_topic'),
    url('^reply/new/(?P<topic_id>\d+)/$', views.new_post, name='lbforum_new_replay'),    
    url('^post/(?P<post_id>\d+)/$', views.post, name='lbforum_post'),    
    url('^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='lbforum_post_edit'),    
    url('^user/(?P<user_id>\d+)/topics/$', views.user_topics, name='lbforum_user_topics'),    
    url('^user/(?P<user_id>\d+)/posts/$', views.user_posts, name='lbforum_user_posts'),    

    url(r'^lang.js$', direct_to_template, {'template': 'lbforum/lang.js'}, name='lbforum_lang_js'),

    url('^markitup_preview/$', views.markitup_preview, name='markitup_preview'),    
)

urlpatterns += patterns('',
    url(r'^account/$', login_required(accountviews.profile), name='lbforum_account_index'),
    url(r'^account/signature/$', accountviews.signature, name='lbforum_signature'),
    (r'^accounts/avatar/', include('simpleavatar.urls')),
)

urlpatterns += patterns('simpleavatar.views',
        url('^account/avatar/change/$', 'change', {'template_name': 'lbforum/account/avatar/change.html'}, \
                name='lbforum_avatar_change'),
)

