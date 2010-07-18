from django import forms
from django.utils.translation import ugettext_lazy as _

from lbforum.models import LBForumUserProfile

class SignatureForm(forms.ModelForm):
    signature = forms.CharField(label=_('Message'), required=False,\
            widget=forms.Textarea(attrs={'cols':'65', 'rows':'4'}))

    class Meta:
        model = LBForumUserProfile
        fields = ('signature',)
