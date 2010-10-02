from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Topic, Post

class PostForm(forms.ModelForm):
    subject = forms.CharField(label=_('Subject'), \
            widget=forms.TextInput(attrs={'size':'80'}))
    message = forms.CharField(label=_('Message'), \
            widget=forms.Textarea(attrs={'cols':'95', 'rows':'14'}))
    attachments = forms.Field(label=_('Attachments'), required=False,\
            widget=forms.SelectMultiple())
    need_replay = forms.BooleanField(label=_('Need Reply'), required=False)
    need_reply_attachments = forms.BooleanField(label=_('Attachments Need Reply'), required=False)

    class Meta:
        model = Post
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        self.forum = kwargs.pop('forum', None)
        self.ip = kwargs.pop('ip', None)
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['subject', 'message', 'attachments', 'need_replay', 
                'need_reply_attachments']

class EditPostForm(PostForm):
    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.initial['subject'] = self.instance.topic.subject
        self.initial['need_replay'] = self.instance.topic.need_replay
        self.initial['need_reply_attachments'] = self.instance.topic.need_reply_attachments
        if not self.instance.topic_post:
            self.fields['subject'].required = False

    def save(self):
        post = self.instance
        post.message = self.cleaned_data['message']
        post.updated_on = datetime.now()
        post.edited_by = self.user.username
        attachments = self.cleaned_data['attachments']
        post.update_attachments(attachments)
        post.save()
        if post.topic_post:
            post.topic.subject = self.cleaned_data['subject']
            post.topic.need_replay = self.cleaned_data['need_replay']
            post.topic.need_reply_attachments = self.cleaned_data['need_reply_attachments']
            post.topic.save()
        return post

class NewPostForm(PostForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        if self.topic:
            self.fields['subject'].required = False

    def save(self):
        topic_post = False
        if not self.topic:
            topic = Topic(forum=self.forum,
                          posted_by=self.user,
                          subject=self.cleaned_data['subject'],
                          need_replay=self.cleaned_data['need_replay'],
                          need_reply_attachments=self.cleaned_data['need_reply_attachments']
                          )
            topic_post = True
            topic.save()
        else:
            topic = self.topic
        post = Post(topic=topic, posted_by=self.user, poster_ip=self.ip,
                    message=self.cleaned_data['message'], topic_post=topic_post)
        post.save()
        attachments = self.cleaned_data['attachments']
        post.update_attachments(attachments)
        return post
