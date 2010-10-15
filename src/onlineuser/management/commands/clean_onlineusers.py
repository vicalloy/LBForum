from  datetime  import datetime, timedelta

from django.core.management.base import BaseCommand
from django.conf import settings

from onlineuser.models import Online

last_online_duration = getattr(settings, 'LAST_ONLINE_DURATION', 900)

class Command(BaseCommand):
    help = "clean unused online user data"
    
    def handle(self, **options):
        now = datetime.now()
        Online.objects.filter(\
                updated_on__lt = now - timedelta(seconds = last_online_duration)\
                ).delete()
