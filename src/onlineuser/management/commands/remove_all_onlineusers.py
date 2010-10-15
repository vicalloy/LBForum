from django.core.management.base import BaseCommand
from django.conf import settings

from onlineuser.models import Online

last_online_duration = getattr(settings, 'LAST_ONLINE_DURATION', 900)

class Command(BaseCommand):
    help = "remve all online user data"
    
    def handle(self, **options):
        Online.objects.all().delete()
