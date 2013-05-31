from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from lbforum import views, accountviews

forum_patterns = patterns(
    '',
    url(r'^(?P<forum_slug>[\w-]+)/$', views.forum, name='lbforum_forum'),
    url(r'^(?P<forum_slug>[\w-]+)/(?P<topic_type>[\w-]+)/$',
        views.forum, name='lbforum_forum'),
    url(r'^(?P<forum_slug>[\w-]+)/(?P<topic_type>[\w-]+)/(?P<topic_type2>[\w-]+)/$',
        views.forum, name='lbforum_forum'),
)

topic_patterns = patterns(
    '',
    url('^(?P<topic_id>\d+)/$', views.topic, name='lbforum_topic'),
    url('^(?P<topic_id>\d+)/delete/$', views.delete_topic,
        name='lbforum_delete_topic'),
    url('^(?P<topic_id>\d+)/update_topic_attr_as_not/(?P<attr>[\w-]+)/$',
        views.update_topic_attr_as_not,
        name='lbforum_update_topic_attr_as_not'),
    url('^new/(?P<forum_id>\d+)/$', views.new_post, name='lbforum_new_topic'),
)

post_patterns = patterns(
    '',
    url('^(?P<post_id>\d+)/$', views.post, name='lbforum_post'),
    url('^(?P<post_id>\d+)/edit/$', views.edit_post, name='lbforum_post_edit'),
    url('^(?P<post_id>\d+)/delete/$', views.delete_post,
        name='lbforum_post_delete'),
)

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='lbforum_index'),
    url(r'^recent/$', views.recent, name='lbforum_recent'),
    (r'^forum/', include(forum_patterns)),
    (r'^topic/', include(topic_patterns)),
    url('^reply/new/(?P<topic_id>\d+)/$', views.new_post,
        name='lbforum_new_replay'),
    (r'^post/', include(post_patterns)),
    url('^user/(?P<user_id>\d+)/topics/$', views.user_topics,
        name='lbforum_user_topics'),
    url('^user/(?P<user_id>\d+)/posts/$', views.user_posts,
        name='lbforum_user_posts'),
    url(r'^lang.js$', direct_to_template, {'template': 'lbforum/lang.js'},
        name='lbforum_lang_js'),
    url('^markitup_preview/$', views.markitup_preview,
        name='markitup_preview'),
)

urlpatterns += patterns(
    '',
    url(r'^account/$', login_required(accountviews.profile),
        name='lbforum_account_index'),
    url(r'^account/signature/$', accountviews.signature,
        name='lbforum_signature'),
    url(r'^user/(?P<user_id>\d+)/$', login_required(accountviews.profile),
        name='lbforum_user_profile'),
)

urlpatterns += patterns(
    'simpleavatar.views',
    url('^account/avatar/change/$', 'change',
        {'template_name': 'lbforum/account/avatar/change.html'},
        name='lbforum_avatar_change'),
    (r'^accounts/avatar/', include('simpleavatar.urls')),
)
