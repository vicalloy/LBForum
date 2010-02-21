import urllib

from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.hashcompat import md5_constructor

from simpleavatar import AVATAR_DEFAULT_URL, AVATAR_GRAVATAR_BACKUP, AVATAR_GRAVATAR_DEFAULT
from simpleavatar.models import avatar_thumbnail_exists, avatar_thumbnail_url

register = template.Library()

def avatar_url(user, size=80):
    """
    get user's avatar url.
    if user=str show default avatar.
    """
    if isinstance(user, User) and avatar_thumbnail_exists(user, size):
        return avatar_thumbnail_url(user, size)
    else:
        if AVATAR_GRAVATAR_BACKUP:
            params = {'s': str(size)}
            if AVATAR_GRAVATAR_DEFAULT:
                params['d'] = AVATAR_GRAVATAR_DEFAULT
            return "http://www.gravatar.com/avatar/%s/?%s" % (
                md5_constructor(user.email).hexdigest(),
                urllib.urlencode(params))
        else:
            return AVATAR_DEFAULT_URL
register.simple_tag(avatar_url)

def avatar(user, size=80):
    alt = unicode(user)
    url = avatar_url(user, size)
    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (url, alt, 
            size, size)
register.simple_tag(avatar)
