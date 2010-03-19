from django import forms

from models import Attachment

class AttachmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.actived = kwargs.pop('actived', False)
        super(AttachmentForm, self).__init__(*args, **kwargs)

    def save(self):
        attachment = super(AttachmentForm, self).save(commit=False)
        attachment.user = self.user
        attachment.actived = self.actived
        attachment.save()        
        return attachment

    class Meta:
        model = Attachment
        fields = ('file',)
