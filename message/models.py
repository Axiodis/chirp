import os
import uuid

from django.contrib.auth.models import User
from django.db import models

from chirp.settings import MEDIA_URL


class TimestampModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('message_images/', filename)


class Message(TimestampModel):
    user = models.ForeignKey(User)
    status = models.TextField(null=False, max_length=140, blank=False)
    image = models.FileField(upload_to=get_file_path,null=True,blank=True)

    def __str__(self):
        return self.status


class Like(TimestampModel):
    user = models.ForeignKey(User)
    message = models.ForeignKey(Message)
    like = models.BooleanField()


class Follow(TimestampModel):
    followed_user = models.ForeignKey(User, related_name='followed')
    following_user = models.ForeignKey(User, related_name='following')
