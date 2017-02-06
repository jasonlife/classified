from __future__ import unicode_literals
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import hashlib
from django.db.models import signals
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from taggit_autosuggest.managers import TaggableManager
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(100, 50)]
    format = 'JPEG'
    options = {'quality': 60}

register.generator('thoughts:thumbnail', Thumbnail)

# Create your models here.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
class bella(models.Model):
    content = models.CharField(max_length=1500)
    user = models.ForeignKey(User, related_name="user")
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to='avatars')
    likes = models.ManyToManyField(User, related_name='likes')
    
    @property
    def total_likes(self):
        """
            Likes for the company
            :return: Integer: Likes for the company
            """
        return self.likes.count()



class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True, related_name="user1")
    tags = TaggableManager()
    
    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

