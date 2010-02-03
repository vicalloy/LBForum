from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Topic, Post

class PostForm(forms.ModelForm):
    subject = forms.CharField(label=_('Subject'), \
            widget=forms.TextInput(attrs={'size':'80'}))
    message = forms.CharField(label=_('Message'), \
            widget=forms.Textarea(attrs={'cols':'95', 'rows':'14'}))

    class Meta:
        model = Post
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        self.forum = kwargs.pop('forum', None)
        self.ip = kwargs.pop('ip', None)
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['subject', 'message']

        if self.topic:
            self.fields['subject'].widget = forms.HiddenInput()
            self.fields['subject'].required = False

    def save(self):
        if not self.topic:
            topic = Topic(forum=self.forum,
                          posted_by=self.user,
                          subject=self.cleaned_data['subject'])
            topic.save()
        else:
            topic = self.topic
        post = Post(topic=topic, posted_by=self.user, poster_ip=self.ip,
                    message=self.cleaned_data['message'])
        post.save()
        return post
