from  datetime  import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

last_online_duration = getattr(settings, 'LAST_ONLINE_DURATION', 900)

class OnlineManager(models.Manager):
    def onlines(self):
        now = datetime.datetime.now()
        return Online.objects.filter(\
                last_activity__gte = now - timedelta(seconds = last_online_duration)\
                )

    def online_users(self):
        return self.onlines.filter(user__isnull=True)

class Online(models.Model):
    user = models.OneToOneField(User, related_name='online', blank=True, null=True)
    ident = models.CharField(max_length=200, unique=True)#username id for user / ip for guest
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = OnlineManager()

    def online(self):
        now = datetime.now()
        if (now - self.updated_on).seconds < last_online_duration:
            return True
        return False   

    def save(self, *args, **kwargs):
        if self.user:
            self.ident = '%s %s' % (self.user.username, self.user.pk)
        super(Online, self).save(*args, **kwargs)
