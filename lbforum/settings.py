from django.conf import settings

STICKY_TOPIC_POST = getattr(settings, 'LBF_STICKY_TOPIC_POST', False)
LAST_TOPIC_NO_INDEX = getattr(settings, 'LBF_LAST_TOPIC_NO_INDEX', False)
