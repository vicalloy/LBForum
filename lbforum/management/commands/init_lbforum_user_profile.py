from django.core.management.base import BaseCommand

from lbforum.models import LBForumUserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Init LBForumUserProfile"
    
    def handle(self, **options):
        users = User.objects.all()
        for o in users:
            #LBForumUserProfile.objects.create(user=instance)
            try:
                o.lbforum_profile
            except LBForumUserProfile.DoesNotExist:
                LBForumUserProfile.objects.create(user=o)
