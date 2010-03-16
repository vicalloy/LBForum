from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Attachment(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Attachment'))
    file = models.FileField(max_length=255, upload_to='')
    actived = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)
