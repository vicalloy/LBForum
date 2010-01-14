#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import Context , loader
from django.template import RequestContext
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.syndication.feeds import Feed
from django.contrib.auth.models import User , Group
from django.conf import settings
from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext_lazy as _

from  datetime  import datetime, timedelta

from models import Topic, Category, Forum, Post, LBForumUserProfile

def index(request, template_name="lbforum/index.html"):
    categories = Category.objects.all()
    total_topics = Topic.objects.count()
    total_posts = Post.objects.count()
    total_users =  User.objects.count()
    last_registered_user = User.objects.order_by('-date_joined')[0]
    ext_ctx = {'users_online': '', 'categories': categories, 'total_topics': total_topics,
            'total_posts': total_posts, 'total_users': total_users,
            'last_registered_user': last_registered_user}
    return render_to_response(template_name, ext_ctx, RequestContext(request))

def forum(request, forum_slug, template_name="lbforum/forum.html"):
    forum = get_object_or_404(Forum, slug = forum_slug)
    topics = Topic.objects.filter(forum__id__exact = forum.id).order_by('-sticky', '-created_on').\
            select_related()
    topic_page_size = getattr(settings , "TOPIC_PAGE_SIZE", 20)#TODO ?
    ext_ctx = {'forum': forum, 'topics': topics}
    return object_list(request,
                       topics,
                       paginate_by = topic_page_size,
                       template_name = template_name,
                       extra_context = ext_ctx,
                       allow_empty = True)

def topic(request, topic_id, template_name="lbforum/topic.html"):
    topic = get_object_or_404(Forum, id = topic_id)
    topic.num_views += 1
    topic.save()
    posts = Post.objects.filter(topic__id__exact = forum.id).order_by('-created_on').\
            select_related()
    topic_page_size = getattr(settings , "POST_PAGE_SIZE", 20)#TODO ?
    ext_ctx = {'topic': topic, 'posts': posts}#TODO first_post
    return object_list(request,
                       posts,
                       paginate_by = topic_page_size,
                       template_name = template_name,
                       extra_context = ext_ctx,
                       allow_empty = True)

#Feed...
#Add Post
#Add Topic
