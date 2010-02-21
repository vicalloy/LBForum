import datetime
import os.path

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage
from django.db.models.signals import post_save

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image

from simpleavatar import AVATAR_STORAGE_DIR, AVATAR_RESIZE_METHOD

def get_file_suffix(filename):
    idx = filename.rfind('.')
    return filename[idx:]

def avatar_file_path(instance=None, filename=None, user=None, size=None):
    user = user or instance.user
    if filename:
        suffix = get_file_suffix(filename)
    fn = '%s_' % user.pk
    if size:
        fn = '%s%s' % (fn, size)
        suffix = '.jpg'
    return os.path.join(AVATAR_STORAGE_DIR, fn+suffix)

def upload_avatar_file_path(*args, **kwargs):
    """
    get avatar_file_path. 
    if exists, remove it first.
    """
    fn = avatar_file_path(*args, **kwargs)
    if default_storage.exists(fn):
        default_storage.delete(fn)
    return fn

def avatar_thumbnail_exists(user, size):
    fn = avatar_file_path(user=user, size=size)
    return default_storage.exists(fn)

def avatar_thumbnail_url(user, size):
    fn = avatar_file_path(user=user, size=size)
    return default_storage.url(fn)

class Avatar(models.Model):
    user = models.OneToOneField(User, related_name='avatar', verbose_name=_('User'))
    avatar = models.ImageField(max_length=1024, upload_to=upload_avatar_file_path, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return _(u'Avatar for %s') % self.user
    
    def thumbnail_exists(self, size):
        return self.avatar.storage.exists(self.avatar_file_path(size))
    
    def create_thumbnail(self, size):
        try:
            orig = self.avatar.storage.open(self.avatar.name, 'rb').read()
            image = Image.open(StringIO(orig))
        except IOError:
            return # What should we do here?  Render a "sorry, didn't work" img?
        (w, h) = image.size
        if w != size or h != size:
            if w > h:
                diff = (w - h) / 2
                image = image.crop((diff, 0, w - diff, h))
            else:
                diff = (h - w) / 2
                image = image.crop((0, diff, w, h - diff))
            image = image.resize((size, size), AVATAR_RESIZE_METHOD)
            if image.mode != "RGB":
                image = image.convert("RGB")
            thumb = StringIO()
            image.save(thumb, "JPEG")
            thumb_file = ContentFile(thumb.getvalue())
        else:
            thumb_file = ContentFile(orig)
        thumb = self.avatar.storage.save(\
                upload_avatar_file_path(instance=self, size=size), \
                thumb_file)
    
    def avatar_url(self, size):
        return self.avatar.storage.url(self.avatar_file_path(size))
    
    def avatar_file_path(self, size):
        return avatar_file_path(instance=self, size=size)

from django.conf import settings
AUTO_GENERATE_AVATAR_SIZES = getattr(settings, 'AUTO_GENERATE_AVATAR_SIZES', (80,))

def create_default_thumbnails(instance=None, created=False, **kwargs):
    #TODO delete old avatar
    for size in AUTO_GENERATE_AVATAR_SIZES:
        instance.create_thumbnail(size)

post_save.connect(create_default_thumbnails, sender=Avatar)
