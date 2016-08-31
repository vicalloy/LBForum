from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers

from lbforum import views, profileviews
from lbforum import api

router = routers.DefaultRouter()
router.register(r'topic', api.TopicViewSet)

forum_patterns = [
    url(r'^(?P<forum_slug>[\w-]+)/$', views.forum, name='lbforum_forum'),
    url(r'^(?P<forum_slug>[\w-]+)/(?P<topic_type>[\w-]+)/$',
        views.forum, name='lbforum_forum'),
    url(r'^(?P<forum_slug>[\w-]+)/(?P<topic_type>[\w-]+)/(?P<topic_type2>[\w-]+)/$',
        views.forum, name='lbforum_forum'),
]

topic_patterns = [
    url('^(?P<topic_id>\d+)/$', views.topic, name='lbforum_topic'),
    url('^(?P<topic_id>\d+)/delete/$', views.delete_topic,
        name='lbforum_delete_topic'),
    url('^(?P<topic_id>\d+)/toggle_topic_attr/(?P<attr>[\w-]+)/$',
        views.toggle_topic_attr,
        name='lbforum_toggle_topic_attr'),
    url('^new/$', views.new_post, name='lbforum_new_topic'),
    url('^new/(?P<forum_id>\d+)/$', views.new_post, name='lbforum_new_topic'),
]

post_patterns = [
    url('^(?P<post_id>\d+)/$', views.post, name='lbforum_post'),
    url('^(?P<post_id>\d+)/edit/$', views.edit_post, name='lbforum_post_edit'),
    url('^(?P<post_id>\d+)/delete/$', views.delete_post,
        name='lbforum_post_delete'),
]

profile_patterns = [
    url(r'^$', profileviews.profile,
        name='lbforum_profile'),
    url(r'^(?P<user_id>\d+)/$', profileviews.profile,
        name='lbforum_profile'),
    url('^(?P<user_id>\d+)/topics/$', profileviews.user_topics,
        name='lbforum_user_topics'),
    url('^(?P<user_id>\d+)/posts/$', profileviews.user_posts,
        name='lbforum_user_posts'),
    url(r'^change/$', profileviews.change_profile,
        name='lbforum_change_profile'),
]

urlpatterns = [
    url(r'^$', views.index, name='lbforum_index'),
    url(r'^recent/$', views.recent, name='lbforum_recent'),
    url(r'^forum/', include(forum_patterns)),
    url(r'^topic/', include(topic_patterns)),
    url(r'^profile/', include(profile_patterns)),
    url(r'^api/', include(router.urls)),

    url('^reply/new/(?P<topic_id>\d+)/$', views.new_post,
        name='lbforum_new_replay'),
    url(r'^post/', include(post_patterns)),
    url(r'^lang.js$', TemplateView.as_view(template_name='lbforum/lang.js'),
        name='lbforum_lang_js'),
    url('^markitup_preview/$', views.markitup_preview,
        name='markitup_preview'),
]
