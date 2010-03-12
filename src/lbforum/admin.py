#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Category, Forum, Topic, Post, LBForumUserProfile

admin.site.register(Category)

def update_forum_nums_topic_post(modeladmin, request, queryset):
    for forum in queryset:
        forum.num_topics = forum.count_nums_topic()
        forum.num_posts = forum.count_nums_post()
        forum.save()
update_forum_nums_topic_post.short_description = "Update topic/post nums"

class ForumAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'category', 'num_topics', \
            'num_posts', )
    list_filter         = ('category',)
    actions = [update_forum_nums_topic_post]

admin.site.register(Forum, ForumAdmin)

class PostInline(admin.TabularInline):
    model = Post

def update_topic_num_replies(modeladmin, request, queryset):
    for topic in queryset:
        topic.num_replies = topic.count_nums_replies()
        topic.save()
update_topic_num_replies.short_description = "Update replies nums"

class TopicAdmin(admin.ModelAdmin):
    list_display        = ('subject', 'forum', 'posted_by', 'sticky', 'closed', \
            'hidden', 'num_views', 'num_replies', 'created_on', 'updated_on', )
    list_filter         = ('forum', 'sticky', 'closed', 'hidden',)
    search_fields       = ('subject', 'posted_by__username', )
    inlines             = (PostInline, )
    actions = [update_topic_num_replies]

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display        = ('__unicode__', 'topic', 'posted_by', 'poster_ip', \
            'created_on', 'updated_on', )
    search_fields       = ('topic__subject', 'posted_by__username', 'message', )

admin.site.register(Post, PostAdmin)

class LBForumUserProfileAdmin(admin.ModelAdmin):
    list_display        = ('user', 'userrank', 'last_activity', 'last_posttime', \
            'signature', )
    search_fields       = ('user', 'userrank', )

admin.site.register(LBForumUserProfile, LBForumUserProfileAdmin)
