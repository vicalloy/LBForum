#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from base64 import b64encode, b64decode
import pickle

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from django.conf import settings

from attachments.models import Attachment
from onlineuser.models import Online

class Config(models.Model):
    key = models.CharField(max_length = 255)#PK
    value = models.CharField(max_length = 255)

class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(default = '')
    ordering = models.PositiveIntegerField(default = 1)    
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(blank = True, null = True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('-ordering', 'created_on')
        
    def __unicode__(self):
        return self.name
    
class Forum(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 110)
    description = models.TextField(default = '')
    ordering = models.PositiveIntegerField(default = 1)
    category = models.ForeignKey(Category)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(blank = True, null = True)
    num_topics = models.IntegerField(default = 0)
    num_posts = models.IntegerField(default = 0)

    last_post = models.CharField(max_length = 255, blank = True)#pickle obj
    
    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
        ordering = ('ordering','-created_on')

    def _count_nums_topic(self):
        return self.topic_set.all().count()

    def _count_nums_post(self):
        return self.topic_set.all().aggregate(Sum('num_replies'))['num_replies__sum'] or 0

    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))
    
    @models.permalink
    def get_absolute_url(self):
        return ('lbforum_forum', (), {'forum_slug': self.slug})

    def __unicode__(self):
        return self.name 

    def update_state_info(self, commit=True):
        self.num_topics = self._count_nums_topic()
        self.num_posts = self._count_nums_post()
        if self.num_topics:
            last_post = Post.objects.all().filter('topic__forum'=self).order_by('-created_on')[0]
            self.last_post = gen_last_post_info(last_post)
        else:
            self.last_post = ''
        if commit:
            self.save()

class TopicType(models.Model):
    forum = models.ForeignKey(Forum, verbose_name=_('Forum'))
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    description = models.TextField(blank=True, default = '')

    def __unicode__(self):
        return self.name 
    
class TopicManager(models.Manager):
    def get_query_set(self):
        return super(TopicManager, self).get_query_set().filter(hidden = False)
    
LEVEL_CHOICES = (
        (30, _('Default')),
        (60, _('Distillate')),
        )

class Topic(models.Model):
    forum = models.ForeignKey(Forum, verbose_name=_('Forum'))
    topic_type = models.ForeignKey(TopicType, verbose_name=_('Topic Type'), 
            blank=True, null=True)
    posted_by = models.ForeignKey(User)
    
    #TODO ADD TOPIC POST.
    post = models.ForeignKey('Post', verbose_name=_('Post'), related_name='topics_',
            blank=True, null=True)
    subject = models.CharField(max_length=999)
    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default=0)#posts...
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    last_reply_on = models.DateTimeField(auto_now_add=True)
    last_post = models.CharField(max_length=255, blank=True)#pickle obj

    has_imgs = models.BooleanField(default=False)
    has_attachments = models.BooleanField(default=False)
    need_replay = models.BooleanField(default=False)#need_reply :-)
    need_reply_attachments = models.BooleanField(default=False)
    
    #Moderation features
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    level = models.SmallIntegerField(choices=LEVEL_CHOICES, default=30)
    
    objects = TopicManager()
    
    class Meta:
        ordering = ('-last_reply_on',)#'-sticky'
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        
    def __unicode__(self):
        return self.subject

    def count_nums_replies(self):
        return self.posts.all().count()
    
    @models.permalink
    def get_absolute_url(self):
        return ('lbforum_topic', (), {'topic_id': self.id})
    
    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))

    def has_replied(self, user):
        if user.is_anonymous():
            return False
        return Post.objects.filter(posted_by=user, topic=self).count()

    def update_state_info(self, commit=True):
        self.num_replies = self.count_nums_replies()
        last_post = self.posts.order_by('-created_on')[0]
        self.last_post = gen_last_post_info(last_post)
        self.save()
        if commit:
            self.save()
        
FORMAT_CHOICES = (
        ('bbcode', _('BBCode')),
        ('html', _('Html')),
        )

# Create Replies for a topic
class Post(models.Model):#can't edit...
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'), related_name='posts')
    posted_by = models.ForeignKey(User)
    poster_ip = models.IPAddressField()
    topic_post = models.BooleanField(default=False)
    
    format = models.CharField(max_length = 20, default='bbcode')#user name
    message = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank = True)

    has_imgs = models.BooleanField(default=False)
    has_attachments = models.BooleanField(default=False)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank = True, null = True)
    edited_by = models.CharField(max_length = 255, blank=True)#user name
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-created_on',)
        get_latest_by = ('created_on', )
        
    def __unicode__(self):
        return self.message[:80]
    
    def subject(self):
        if self.topic_post:
            return _('Topic: %s') % self.topic.subject
        return _('Re: %s') % self.topic.subject

    def file_attachments(self):
        return self.attachments.filter(is_img = False)

    def img_attachments(self):
        return self.attachments.filter(is_img = True)

    def update_attachments_flag(self):
        self.has_attachments = self.file_attachments().count() > 0
        self.has_imgs = self.img_attachments().count() > 0
        self.save()
        if self.topic_post:
            t = self.topic
            t.has_attachments = self.has_attachments
            t.has_imgs = self.has_imgs
            t.save()

    def update_attachments(self, attachment_ids):
        self.attachments.clear()
        for attachment_id in attachment_ids:
            try:
                attachment = Attachment.objects.get(pk=attachment_id)
            except:
                continue
            attachment.activated = True
            attachment.save()
            self.attachments.add(attachment)
        self.update_attachments_flag()

    @models.permalink
    def get_absolute_url(self):
        return ('lbforum_post', (), { 'post_id': self.pk })

    def get_absolute_url_ext(self):
        topic = self.topic
        post_idx = topic.posts.filter(created_on__lte=self.created_on).count()
        page = (post_idx - 1) / settings.CTX_CONFIG['TOPIC_PAGE_SIZE'] + 1
        return '%s?page=%s#p%s' % (topic.get_absolute_url(), page, self.pk)
    
class LBForumUserProfile(models.Model):
    user = models.OneToOneField(User, related_name='lbforum_profile', verbose_name=_('User'))
    last_activity = models.DateTimeField(auto_now_add=True)
    userrank = models.CharField(max_length=30,default="Junior Member")
    last_posttime = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length = 1000, blank = True)
    
    def __unicode__(self):
        return self.user.username
    
    def get_total_posts(self):
        return self.user.post_set.count()

    def get_absolute_url(self):
        return self.user.get_absolute_url()
       
#### smoe function ###

#### do smoe connect ###
def gen_last_post_info(post):
    last_post = {'posted_by': post.posted_by.username, 'update': post.created_on}
    return b64encode(pickle.dumps(last_post, pickle.HIGHEST_PROTOCOL))

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        LBForumUserProfile.objects.create(user=instance)

def update_topic_on_post(sender, instance, created, **kwargs):
    if created:
        t = instance.topic
        t.last_post = gen_last_post_info(instance)
        t.last_reply_on = instance.created_on
        t.num_replies += 1
        t.save()
        p = instance.posted_by.lbforum_profile
        p.last_posttime = instance.created_on
        p.save()

def update_forum_on_post(sender, instance, created, **kwargs):
    if created:
        instance.topic.forum.last_post = gen_last_post_info(instance)
        instance.topic.forum.num_posts += 1
        instance.topic.forum.save()

def update_forum_on_topic(sender, instance, created, **kwargs):
    if created:
        instance.forum.num_topics += 1
        instance.forum.save()

def update_user_last_activity(sender, instance, created, **kwargs):
    if instance.user:
        p = instance.user.lbforum_profile
        p.last_activity = instance.updated_on
        p.save()

post_save.connect(create_user_profile, sender = User)
post_save.connect(update_topic_on_post, sender = Post)
post_save.connect(update_forum_on_post, sender = Post)
post_save.connect(update_forum_on_topic, sender = Topic)
post_save.connect(update_user_last_activity, sender = Online)
