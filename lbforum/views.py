#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
#from django.contrib import messages

from forms import EditPostForm, NewPostForm, ForumForm
from models import Topic, Forum, Post
import settings as lbf_settings

def index(request, template_name="lbforum/index.html"):
    ctx = {}
    if lbf_settings.LAST_TOPIC_NO_INDEX: 
        ctx['topics'] = Topic.objects.all().order_by('-last_reply_on')[:20]
    return render(request, template_name, ctx)

def recent(request, template_name="lbforum/recent.html"):
    ctx = {}
    ctx['topics'] = Topic.objects.all().order_by('-last_reply_on').select_related()
    return render(request, template_name, ctx)

def forum(request, forum_slug, topic_type='', topic_type2='',
        template_name="lbforum/forum.html"):
    forum = get_object_or_404(Forum, slug = forum_slug)
    topics = forum.topic_set.all()
    if topic_type and topic_type != 'good':
        topic_type2 = topic_type
        topic_type = ''
    if topic_type == 'good':
        topics = topics.filter(level__gt = 30)
        #topic_type = _("Distillate District")
    if topic_type2:
        topics = topics.filter(topic_type__slug = topic_type2)
    order_by = request.GET.get('order_by', '-last_reply_on')
    topics = topics.order_by('-sticky', order_by).select_related()
    form = ForumForm(request.GET)
    ext_ctx = {'form': form, 'forum': forum, 'topics': topics, 
            'topic_type': topic_type, 'topic_type2': topic_type2}
    return render(request, template_name, ext_ctx)

def topic(request, topic_id, template_name="lbforum/topic.html"):
    topic = get_object_or_404(Topic, id = topic_id)
    topic.num_views += 1
    topic.save()
    posts = topic.posts
    if lbf_settings.STICKY_TOPIC_POST:#sticky topic post
        posts = posts.filter(topic_post=False)
    posts = posts.order_by('created_on').select_related()
    ext_ctx = {'topic': topic, 'posts': posts}
    ext_ctx['has_replied'] = topic.has_replied(request.user)
    return render(request, template_name, ext_ctx)

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponseRedirect(post.get_absolute_url_ext())

@csrf_exempt
def markitup_preview(request, template_name="lbforum/markitup_preview.html"):
    return render(request, template_name, {'message': request.POST['data']})

@login_required
def new_post(request, forum_id=None, topic_id=None, form_class=NewPostForm, \
        template_name='lbforum/post.html'):
    qpost = topic = forum = first_post = preview = None
    post_type = _('topic')
    topic_post = True
    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        post_type = _('reply')
        topic_post = False
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum
        first_post = topic.posts.order_by('created_on').select_related()[0]
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
        initial={}
        qid = request.GET.get('qid', '')
        if qid:
            qpost = get_object_or_404(Post, id=qid)
            initial['message'] = "[quote=%s]%s[/quote]" % (qpost.posted_by.username, qpost.message)
        form = form_class(initial=initial, forum=forum)
    ext_ctx = {'forum':forum, 'form':form, 'topic':topic, 'first_post':first_post, \
            'post_type':post_type, 'preview':preview}
    ext_ctx['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
    ext_ctx['is_new_post'] = True
    ext_ctx['topic_post'] = topic_post
    ext_ctx['session_key'] = request.session.session_key
    return render(request, template_name, ext_ctx)

@login_required
def edit_post(request, post_id, form_class=EditPostForm, template_name="lbforum/post.html"):
    preview = None
    post_type = _('reply')
    edit_post = get_object_or_404(Post, id=post_id)
    if not (request.user.is_staff or request.user == edit_post.posted_by):
        return HttpResponse(ugettext('no right'))
    if edit_post.topic_post:
        post_type = _('topic')
    if request.method == "POST":
        form = form_class(instance=edit_post, user=request.user, data=request.POST)
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            edit_post = form.save()
            return HttpResponseRedirect('../')
    else:
        form = form_class(instance=edit_post)
    ext_ctx = {'form':form, 'post': edit_post, 'topic':edit_post.topic, \
            'forum':edit_post.topic.forum, 'post_type':post_type, 'preview':preview}
    ext_ctx['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
    ext_ctx['topic_post'] = edit_post.topic_post
    ext_ctx['session_key'] = request.session.session_key
    return render(request, template_name, ext_ctx)

@login_required
def user_topics(request, user_id, template_name='lbforum/account/user_topics.html'):
    view_user = User.objects.get(pk=user_id)
    topics = view_user.topic_set.order_by('-created_on').select_related()
    return render(request, template_name, {'topics': topics, 'view_user': view_user})

@login_required
def user_posts(request, user_id, template_name='lbforum/account/user_posts.html'):
    view_user = User.objects.get(pk=user_id)
    posts = view_user.post_set.order_by('-created_on').select_related()
    return render(request, template_name, {'posts': posts, 'view_user': view_user})

@login_required
def delete_topic(request, topic_id):
    if not request.user.is_staff:
        #messages.error(_('no right'))
        return HttpResponse(ugettext('no right'))
    topic = get_object_or_404(Topic, id = topic_id)
    forum = topic.forum
    topic.delete()
    forum.update_state_info()
    return HttpResponseRedirect(reverse("lbforum_forum", args=[forum.slug]))

@login_required
def delete_post(request, post_id):
    if not request.user.is_staff:
        return HttpResponse(ugettext('no right'))
    post = get_object_or_404(Post, id=post_id)
    topic = post.topic
    post.delete()
    topic.update_state_info()
    topic.forum.update_state_info()
    #return HttpResponseRedirect(request.path)
    return HttpResponseRedirect(reverse("lbforum_topic", args=[topic.id]))

@login_required
def update_topic_attr_as_not(request, topic_id, attr):
    if not request.user.is_staff:
        return HttpResponse(ugettext('no right'))
    topic = get_object_or_404(Topic, id = topic_id)
    if attr == 'sticky':
        topic.sticky = not topic.sticky
    elif attr == 'close':
        topic.closed = not topic.closed
    elif attr == 'hide':
        topic.hidden = not topic.hidden
    elif attr == 'distillate':
        topic.level = 30 if topic.level >= 60 else 60
    topic.save()
    if topic.hidden:
        return HttpResponseRedirect(reverse("lbforum_forum", args=[topic.forum.slug]))
    else:
        return HttpResponseRedirect(reverse("lbforum_topic", args=[topic.id]))

#Feed...
#Add Post
#Add Topic
