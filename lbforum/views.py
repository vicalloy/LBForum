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

from models import Topic, Category, Forum, Post, LBForumProfile

def index(request):
    forums = Category.objects.all()
    total_topics = Topic.objects.count()
    total_posts = Post.objects.count()
    total_users =  User.objects.count()
    last_registered_user = User.objects.order_by('-date_joined')[0]
    ext_ctx = {'users_online': '', 'forums_list': forums, 'total_topics': total_topics,
            'total_posts': total_posts, 'total_users': total_users, 
            'last_registered_user': last_registered_user}
    return render_to_response("lbforum/index.html", ext_ctx, RequestContext(request))
