from django.core.management.base import BaseCommand

from lbforum.models import Topic

class Command(BaseCommand):
    help = "update topic/post's base info."
    
    def handle(self, **options):
        topics = Topic.objects.all()
        for t in topics:
            post = t.posts.order_by('created_on').all()[0]
            t.post = post
            t.save()
