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

        if self.topic:
            self.fields['subject'].widget = forms.HiddenInput()
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
        for attachment_id in attachments:
            try:
                attachment = Attachment.objects.get(pk=attachment_id)
            except:
                continue
            attachment.activated = True
            attachment.save()
            post.attachments.add(attachment)
        return post
