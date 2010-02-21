from django import forms
from models import Avatar

class AvatarForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        instance = None
        try:
            instance = self.user.avatar
        except Exception, e:
            pass
        super(AvatarForm, self).__init__(instance=instance, *args, **kwargs)

    class Meta:
        model = Avatar
        fields = ('avatar',)

    def save(self):
        avatar = super(AvatarForm, self).save(commit=False)
        avatar.user = self.user
        avatar.save()
