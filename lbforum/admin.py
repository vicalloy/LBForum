# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Category, Forum, TopicType, Topic
from .models import Post, LBForumUserProfile

admin.site.register(Category)


def update_forum_state_info(modeladmin, request, queryset):
    for forum in queryset:
        forum.update_state_info()
update_forum_state_info.short_description = _("Update forum state info")


class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'num_topics', 'num_posts',)
    list_filter = ('category',)
    raw_id_fields = ('admins', 'last_post')
    actions = [update_forum_state_info]

admin.site.register(Forum, ForumAdmin)


class TopicTypeAdmin(admin.ModelAdmin):
    list_display = ('forum', 'name', 'slug', 'description', )
    list_filter = ('forum',)

admin.site.register(TopicType, TopicTypeAdmin)


class PostInline(admin.TabularInline):
    model = Post


def update_topic_state_info(modeladmin, request, queryset):
    for topic in queryset:
        topic.update_state_info()
update_topic_state_info.short_description = _("Update topic state info")


def update_topic_attr_as_not(modeladmin, request, queryset, attr):
    for topic in queryset:
        if attr == 'sticky':
            topic.sticky = not topic.sticky
        elif attr == 'close':
            topic.closed = not topic.closed
        elif attr == 'hide':
            topic.hidden = not topic.hidden
        topic.save()


def sticky_unsticky_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'sticky')
sticky_unsticky_topic.short_description = _("sticky/unsticky topics")


def close_unclose_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'close')
close_unclose_topic.short_description = _("close/unclose topics")


def hide_unhide_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'hide')
hide_unhide_topic.short_description = _("hide/unhide topics")


class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'subject', 'forum', 'topic_type', 'posted_by', 'sticky', 'closed',
        'hidden', 'level', 'num_views', 'num_replies', 'created_on', 'updated_on', )
    list_filter = ('forum', 'sticky', 'closed', 'hidden', 'level')
    search_fields = ('subject', 'posted_by__username', )
    # inlines = (PostInline, )
    raw_id_fields = ('posted_by', 'post', 'last_post')
    actions = [update_topic_state_info, sticky_unsticky_topic, close_unclose_topic, hide_unhide_topic]

admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'topic', 'posted_by', 'poster_ip',
        'created_on', 'updated_on', )
    search_fields = ('topic__subject', 'posted_by__username', 'message', )
    raw_id_fields = ('topic', 'posted_by', 'attachments', 'last_updated_by')
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        for o in obj.all():
            topic = o.topic
            o.delete()
            topic.update_state_info()
    delete_model.short_description = 'Delete posts'

admin.site.register(Post, PostAdmin)


class LBForumUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'bio',)
    search_fields = ('user__username', 'nickname', )
    raw_id_fields = ('user',)

admin.site.register(LBForumUserProfile, LBForumUserProfileAdmin)
