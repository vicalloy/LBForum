from django.core.management.base import BaseCommand

from lbforum.models import Topic, Post

class Command(BaseCommand):
    help = "update topic/post's base info."
    
    def handle(self, **options):
        posts = Post.objects.all()
        for o in posts:
            o.update_attachments_flag()
