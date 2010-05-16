from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Topic, Post
from attachments.models import Attachment

class PostForm(forms.ModelForm):
    subject = forms.CharField(label=_('Subject'), \
            widget=forms.TextInput(attrs={'size':'80'}))
    message = forms.CharField(label=_('Message'), \
            widget=forms.Textarea(attrs={'cols':'95', 'rows':'14'}))
    attachments = forms.Field(label=_('Attachments'), required=False,\
            widget=forms.SelectMultiple())

    class Meta:
        model = Post
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        self.forum = kwargs.pop('forum', None)
        self.ip = kwargs.pop('ip', None)
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['subject', 'message', 'attachments']

class EditPostForm(PostForm):
    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.initial['subject'] = self.instance.topic.subject
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
                          subject=self.cleaned_data['subject'])
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
