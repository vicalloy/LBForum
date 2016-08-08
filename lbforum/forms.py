# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from constance import config
from .models import Topic, Post, TopicType
from .models import LBForumUserProfile
from .models import Forum
from .models import Category

FORUM_ORDER_BY_CHOICES = (
    ('-last_reply_on', _('Last Reply')),
    ('-created_on', _('Last Topic')),
)


class ForumChoiceFieldMixin(object):

    def _get_choices(self):
        # def init_choices(self, have_blank=True, **kwargs):
        have_blank = True
        empty_label = self.empty_label
        categories = Category.objects.all().order_by('oid')
        choices = []
        if empty_label and have_blank:
            choices.append(['', empty_label])
        try:  # if table not existed will fail.
            for category in categories:
                choices.append(
                    (category.name, [(e.pk, e.name) for e in category.forum_set.all()])
                )
        except:
            pass
        return choices


class ForumChoiceField(ForumChoiceFieldMixin, forms.ModelChoiceField):

    choices = property(ForumChoiceFieldMixin._get_choices, None)

    def __init__(self, *args, **kwargs):
        qs = Forum.objects.all()
        self.empty_label = kwargs.pop('empty_label', '------')
        super(ForumChoiceField, self).__init__(*args, queryset=qs, **kwargs)
        # self.init_choices(True, **kwargs)


class ForumForm(forms.Form):
    order_by = forms.ChoiceField(label=_('Order By'), choices=FORUM_ORDER_BY_CHOICES, required=False)


class PostForm(forms.ModelForm):
    forum = ForumChoiceField(label=_('Forum'), required=False)
    topic_type = forms.ChoiceField(label=_('Topic Type'), required=False)
    subject = forms.CharField(label=_('Subject'), widget=forms.TextInput(attrs={'size': '80'}))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={'cols': '95', 'rows': '14'}))
    attachments = forms.Field(label=_('Attachments'), required=False, widget=forms.SelectMultiple())
    need_replay = forms.BooleanField(label=_('Need Reply'), required=False)
    need_reply_attachments = forms.BooleanField(label=_('Attachments Need Reply'), required=False)

    class Meta:
        model = Post
        fields = ('message', )

    def clean_forum(self):
        forum = self.cleaned_data['forum']
        forum = forum or self.forum
        if not forum:
            raise forms.ValidationError(_('Please chose a forum'))
        self.forum = forum
        return forum

    def clean_message(self):
        msg = self.cleaned_data['message']
        forbidden_words = config.forbidden_words
        for word in forbidden_words.split(','):
            word = word.strip()
            if word and word in msg:
                raise forms.ValidationError(_('Some word in you post is forbidden, please correct it.'))
        return msg

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        forum = kwargs.pop('forum', None)
        if self.topic:
            forum = self.topic.forum
        self.ip = kwargs.pop('ip', None)
        self.forum = forum or getattr(self, 'forum', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if self.forum:
            topic_types = self.forum.topictype_set.all()
            self.fields['topic_type'].choices = [(tp.id, tp.name) for tp in topic_types]
            self.fields['topic_type'].choices.insert(0, (('', '--------')))
        self.fields.keyOrder = [
            'topic_type', 'subject', 'message', 'attachments', 'need_replay',
            'need_reply_attachments']


class EditPostForm(PostForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        initial = kwargs.pop('initial', {})
        initial['subject'] = instance.topic.subject
        self.forum = instance.topic.forum
        initial['forum'] = self.forum
        initial['need_replay'] = instance.topic.need_replay
        initial['need_reply_attachments'] = instance.topic.need_reply_attachments
        if instance.topic.topic_type:
            initial['topic_type'] = instance.topic.topic_type.id
        super(EditPostForm, self).__init__(*args, instance=instance, initial=initial, **kwargs)
        if not instance.topic_post:
            self.fields['subject'].required = False

    def save(self):
        post = self.instance
        post.message = self.cleaned_data['message']
        post.updated_on = datetime.now()
        post.edited_by = self.user.lbforum_profile.nickname
        attachments = self.cleaned_data['attachments']
        post.update_attachments(attachments)
        post.save()
        if post.topic_post:
            topic = post.topic
            topic.forum = self.forum
            topic.subject = self.cleaned_data['subject']
            topic.need_replay = self.cleaned_data['need_replay']
            topic.need_reply_attachments = self.cleaned_data['need_reply_attachments']
            topic_type = self.cleaned_data['topic_type']
            if topic_type:
                topic_type = TopicType.objects.get(id=topic_type)
            else:
                topic_type = None
            topic.topic_type = topic_type
            topic.save()
        return post


class NewPostForm(PostForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        if self.topic:
            self.fields['subject'].required = False

    def save(self):
        topic_post = False
        if not self.topic:
            topic_type = self.cleaned_data['topic_type']
            if topic_type:
                topic_type = TopicType.objects.get(id=topic_type)
            else:
                topic_type = None
            topic = Topic(forum=self.forum,
                          posted_by=self.user,
                          subject=self.cleaned_data['subject'],
                          need_replay=self.cleaned_data['need_replay'],
                          need_reply_attachments=self.cleaned_data['need_reply_attachments'],
                          topic_type=topic_type,
                          )
            topic_post = True
            topic.save()
        else:
            topic = self.topic
        post = Post(topic=topic, posted_by=self.user, poster_ip=self.ip,
                    message=self.cleaned_data['message'], topic_post=topic_post)
        post.save()
        if topic_post:
            topic.post = post
            topic.save()
        attachments = self.cleaned_data['attachments']
        post.update_attachments(attachments)
        return post


class SignatureForm(forms.ModelForm):
    signature = forms.CharField(
        label=_('Message'), required=False,
        widget=forms.Textarea(attrs={'cols': '65', 'rows': '4'}))

    class Meta:
        model = LBForumUserProfile
        fields = ('signature',)


class ProfileForm(forms.ModelForm):
    signature = forms.CharField(
        label=_('Message'), required=False,
        widget=forms.Textarea(attrs={'rows': '4'}))

    class Meta:
        model = LBForumUserProfile
        fields = ('avatar', 'nickname', 'signature', 'bio')
