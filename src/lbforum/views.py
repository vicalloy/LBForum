#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from onlineuser.models import getOnlineInfos
from forms import PostForm
from models import Topic, Category, Forum, Post

def index(request, template_name="lbforum/index.html"):
    categories = Category.objects.all()
    total_topics = Topic.objects.count()
    total_posts = Post.objects.count()
    total_users =  User.objects.count()
    last_registered_user = User.objects.order_by('-date_joined')[0]
    ext_ctx = {'categories': categories, 'total_topics': total_topics,
            'total_posts': total_posts, 'total_users': total_users,
            'last_registered_user': last_registered_user}
    ext_ctx.update(getOnlineInfos(True))
    return render_to_response(template_name, ext_ctx, RequestContext(request))

def forum(request, forum_slug, template_name="lbforum/forum.html"):
    forum = get_object_or_404(Forum, slug = forum_slug)
    topics = forum.topic_set.order_by('-sticky', '-last_reply_on').select_related()
    ext_ctx = {'forum': forum, 'topics': topics}
    return render_to_response(template_name, ext_ctx, RequestContext(request))

def topic(request, topic_id, template_name="lbforum/topic.html"):
    topic = get_object_or_404(Topic, id = topic_id)
    topic.num_views += 1
    topic.save()
    posts = topic.post_set.order_by('created_on').select_related()
    ext_ctx = {'topic': topic, 'posts': posts}
    return render_to_response(template_name, ext_ctx, RequestContext(request))

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponseRedirect(post.get_absolute_url_ext())

@login_required
def new_post(request, forum_id=None, topic_id=None, form_class=PostForm, template_name='lbforum/new_post.html'):
    topic = forum = first_post = preview = None
    action_type = 'topic'
    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        action_type = 'reply'
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum
        first_post = topic.post_set.order_by('created_on').select_related()[0]
    if request.method == "POST":
        form = form_class(request.POST, user=request.user, forum=forum, topic=topic, \
                ip=request.META['REMOTE_ADDR'])
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            post = form.save()
            if topic:
                return HttpResponseRedirect(post.get_absolute_url_ext())
            else:
                return HttpResponseRedirect(reverse("lbforum_forum", args=[forum.slug]))
    else:
        form = form_class()
    ext_ctx = {'forum':forum, 'form':form, 'topic':topic, 'first_post':first_post, \
            'action_type':action_type, 'preview':preview}
    return render_to_response(template_name, ext_ctx, RequestContext(request))

@login_required
def user_topics(request, user_id, template_name='lbforum/user_topics.html'):
    view_user = User.objects.get(pk=user_id)
    topics = view_user.topic_set.order_by('-created_on').select_related()
    return render_to_response(template_name, {'topics': topics, 'view_user': view_user}, \
            RequestContext(request))

@login_required
def user_posts(request, user_id, template_name='lbforum/user_posts.html'):
    view_user = User.objects.get(pk=user_id)
    posts = view_user.post_set.order_by('-created_on').select_related()
    return render_to_response(template_name, {'posts': posts, 'view_user': view_user}, \
            RequestContext(request))
#Feed...
#Add Post
#Add Topic
