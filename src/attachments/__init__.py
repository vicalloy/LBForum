from django.conf import settings

ATTACHMENT_STORAGE_DIR = getattr(settings, 'ATTACHMENT_STORAGE_DIR', 'attachments')
