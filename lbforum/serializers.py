# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Topic
from .models import Post
from .models import Forum

User = get_user_model()


class ForumSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('slug', 'name', )
        model = Forum


class UserSimpleSerializer(serializers.ModelSerializer):
    # lbforum_profile = LBForumUserProfileSimpleSerializer()
    nickname = serializers.SerializerMethodField()

    class Meta:
        fields = ('pk', 'username', 'nickname', )
        model = User

    def get_nickname(self, obj):
        try:
            return obj.lbforum_profile.nickname
        except AttributeError:
            return None


class PostSimpleSerializer(serializers.ModelSerializer):
    posted_by = UserSimpleSerializer()

    class Meta:
        model = Post
        fields = ('posted_by', 'created_on', )
        # depth = 2


class TopicSerializer(serializers.ModelSerializer):
    forum = ForumSimpleSerializer()
    posted_by = UserSimpleSerializer()
    last_post = PostSimpleSerializer()

    class Meta:
        model = Topic
        fields = (
            'subject', 'forum', 'topic_type', 'posted_by', 'sticky', 'closed',
            'hidden', 'level', 'num_views', 'num_replies', 'created_on', 'updated_on',
            'last_post', )
        # depth = 2
