#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Category, Forum, Topic, Post, LBForumUserProfile

admin.site.register(Category)

class ForumAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'category', 'num_topics', \
            'num_posts', )
    list_filter         = ('category',)

admin.site.register(Forum, ForumAdmin)

class PostInline(admin.TabularInline):
    model = Post

class TopicAdmin(admin.ModelAdmin):
    list_display        = ('subject', 'forum', 'posted_by', 'sticky', 'closed', \
            'hidden', 'num_views', 'num_replies', 'created_on', 'updated_on', )
    list_filter         = ('forum', 'sticky', 'closed', 'hidden',)
    search_fields       = ('subject', 'posted_by', )
    inlines             = (PostInline, )

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display        = ('__unicode__', 'topic', 'posted_by', 'poster_ip', \
            'created_on', 'updated_on', )
    search_fields       = ('topic', 'posted_by', 'message', )

admin.site.register(Post, PostAdmin)

class LBForumUserProfileAdmin(admin.ModelAdmin):
    list_display        = ('user', 'userrank', 'last_activity', 'last_posttime', \
            'signature', )
    search_fields       = ('user', 'userrank', )

admin.site.register(LBForumUserProfile, LBForumUserProfileAdmin)
