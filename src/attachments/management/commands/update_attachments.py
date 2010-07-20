from django.core.management.base import BaseCommand

from attachments.models import Attachment, get_file_suffix, \
        is_img

class Command(BaseCommand):
    help = "update attachment's base info."
    
    def handle(self, **options):
        attachments = Attachment.objects.all()
        for o in attachments:
            if o.file.storage.exists(o.file.name):
                o.suffix = get_file_suffix(o.file.name)
                o.is_img = is_img(o.suffix)
                o.file_size = o.file.size
                o.save()
            else:
                o.file_size = -1
                o.save()
