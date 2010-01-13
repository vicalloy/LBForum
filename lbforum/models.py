#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

import pickle
from BeautifulSoup import BeautifulSoup
from postmarkup import render_bbcode

class Config(models.Model):
    key = models.CharField(max_length = 255)#PK
    value = models.CharField(max_length = 255)

class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(default = '')
    ordering = models.PositiveIntegerField(default = 1)    
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    
    class Meta:
        verbose_name = _("Category)")
        verbose_name_plural = _("Categories")
        ordering = ('-ordering', 'created_on')
        
    def __unicode__(self):
        return self.name
    
class Forum(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 110)#unic...
    description = models.TextField(default = '')
    ordering = models.PositiveIntegerField(default = 1)
    category = models.ForeignKey(Category)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    num_topics = models.IntegerField(default = 0)
    num_posts = models.IntegerField(default = 0)

    last_post = models.CharField(max_length = 255, blank = True)#pickle obj
    __last_post = ""
    
    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
        ordering = ('ordering','-created_on')

    def get_last_post(self):
        if not __last_post:
            __last_post = pickle.loads(self.last_post)
        return __last_post
    
    @models.permalink
    def get_absolute_url(self):
        return ('lbforum_index', (), {'forumslug': self.slug})

    def __unicode__(self):
        return self.name 
    
class TopicManager(models.Manager):
    def get_query_set(self):
        return super(TopicManager, self).get_query_set().filter(hidden = False)
    
class Topic(models.Model):
    forum = models.ForeignKey(Forum)
    posted_by = models.ForeignKey(User)
    
    subject = models.CharField(max_length=999)
    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default = -1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    last_post = models.CharField(max_length = 255)#pickle obj
    __last_post = ""
    
    #Moderation features
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    
    objects = TopicManager()
    
    class Meta:
        ordering = ('-sticky', '-last_reply_on',)
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        
    def __unicode__(self):
        return self.subject
    
    @models.permalink
    def get_absolute_url(self):
        return ('lbforum_topic_detail', (), {'forumslug': self.forum.slug, 'topic_id': self.id})
    
    def htmlfrombbcode(self):#TODO bbcode or html in db?
        if self.message.strip():
            return render_bbcode(self.message)
        else :
            return ""

    def get_last_post(self):
        if not __last_post:
            __last_post = pickle.loads(self.last_post)
        return __last_post
        
# Create Replies for a topic
class Post(models.Model):#can't edit...
    topic = models.ForeignKey(Topic)
    posted_by = models.ForeignKey(User)
    poster_ip = models.IPAddressField()
    
    #TODO add html/rst/..suport
    message = models.TextField()
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    edited_by = models.CharField(max_length = 255)#user name
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('created_on',)
        get_latest_by = ('created_on', )
        
    def __unicode__(self):
        return self.message
    
    @models.permalink
    def get_absolute_url(self):
        return ('lbforum_topic_detail', (), {'forumslug': self.topic.forum.slug, 'topic_slug': self.topic.slug})
    
    def htmlfrombbcode(self):
        soup = BeautifulSoup(self.message)
        #remove all html tags from the message
        onlytext = ''.join(soup.findAll(text=True))
        
        #get the bbcode for the text
        if onlytext.strip():
            return render_bbcode(onlytext)
        else :
            return ""
        
class LBForumUserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    last_activity = models.DateTimeField(auto_now_add=True)
    userrank = models.CharField(max_length=30,default=_("Junior Member"))
    last_posttime = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length = 1000, null = True, blank = True)
    
    def __unicode__(self):
        return self.user.username
    
    def get_total_posts(self):
        return self.user.post_set.count()

    def get_absolute_url(self):
        return self.user.get_absolute_url()
       

class Online(models.Model):
    #TODO how to use?
    user = models.ForeignKey(User, blank = True)
    ident = models.CharField(max_length=200)
    idle = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

#### do smoe connect ###
def gen_last_post_info(post):
    last_post = {'posted_by': post.posted_by.username, 'update': post.created_on}
    return pickle.dumps(last_post, pickle.HIGHEST_PROTOCOL)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        LBForumUserProfile.objects.create(user=instance)

def update_topic_on_post(sender, instance, created, **kwargs):
    if created:
        instance.topic.last_post = gen_last_post_info(instance)
        instance.topic.last_reply_on = instance.created_on
        instance.topic.num_replies += 1
        instance.topic.save()

def update_forum_on_post(sender, instance, created, **kwargs):
    if created:
        instance.forum.last_post = gen_last_post_info(instance)
        instance.forum.num_topics += 1
        instance.forum.num_posts += 1
        instance.forum.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(update_topic_on_post, sender=Post)
post_save.connect(update_forum_on_post, sender=Post)
