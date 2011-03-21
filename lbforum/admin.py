#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Category, Forum, TopicType, Topic, Post, LBForumUserProfile

admin.site.register(Category)

def update_forum_nums_topic_post(modeladmin, request, queryset):
    for forum in queryset:
        forum.num_topics = forum.count_nums_topic()
        forum.num_posts = forum.count_nums_post()
        if forum.num_topics:
            forum.last_post = forum.topic_set.order_by('-last_reply_on')[0].last_post
        else:
            forum.last_post = ''
        forum.save()
update_forum_nums_topic_post.short_description = _("Update topic/post nums")

class ForumAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'category', 'num_topics', \
            'num_posts', )
    list_filter         = ('category',)
    actions = [update_forum_nums_topic_post]

admin.site.register(Forum, ForumAdmin)

class TopicTypeAdmin(admin.ModelAdmin):
    list_display        = ('forum', 'name', 'slug', 'description', )
    list_filter         = ('forum',)

admin.site.register(TopicType, TopicTypeAdmin)

class PostInline(admin.TabularInline):
    model = Post

def update_topic_num_replies(modeladmin, request, queryset):
    for topic in queryset:
        topic.num_replies = topic.count_nums_replies()
        topic.save()
update_topic_num_replies.short_description = _("Update replies nums")

def update_topic_attr_as_not(modeladmin, request, queryset, attr):
    for topic in queryset:
        if attr == 'sticky':
            topic.sticky = not topic.sticky
        elif attr == 'closed':
            topic.closed = not topic.closed
        elif attr == 'hidden':
            topic.hidden = not topic.hidden
        topic.save()

def sticky_unsticky_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'sticky')
sticky_unsticky_topic.short_description = _("sticky/unsticky topics")

def close_unclose_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'closed')
close_unclose_topic.short_description = _("close/unclose topics")

def hide_unhide_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'hidden')
hide_unhide_topic.short_description = _("hide/unhide topics")

class TopicAdmin(admin.ModelAdmin):
    list_display        = ('subject', 'forum', 'topic_type', 'posted_by', 'sticky', 'closed',
            'hidden', 'level', 'num_views', 'num_replies', 'created_on', 'updated_on', )
    list_filter         = ('forum', 'sticky', 'closed', 'hidden', 'level')
    search_fields       = ('subject', 'posted_by__username', )
    #inlines             = (PostInline, )
    actions = [update_topic_num_replies, sticky_unsticky_topic, close_unclose_topic, 
            hide_unhide_topic]

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display        = ('__unicode__', 'topic', 'posted_by', 'poster_ip', \
            'created_on', 'updated_on', )
    search_fields       = ('topic__subject', 'posted_by__username', 'message', )

admin.site.register(Post, PostAdmin)

class LBForumUserProfileAdmin(admin.ModelAdmin):
    list_display        = ('user', 'userrank', 'last_activity', 'last_posttime', \
            'signature', )
    search_fields       = ('user__username', 'userrank', )

admin.site.register(LBForumUserProfile, LBForumUserProfileAdmin)
