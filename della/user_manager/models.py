from django.db import models
from django.contrib.auth.models import User

from della.utils import TimeStampMixin


def avatar_file_name(instance, filename):
    ext = filename.split('.')[-1]
    file_name = "{}.{}".format(instance.user.username, ext)
    return "{}/{}".format('avatars', file_name)


class UserProfile(TimeStampMixin):
    """
    To manage users and stuff. From default `User` we will use `username`,
    `email`, `password`, `first_name` and `last_name`.
    """
    bio = models.TextField(null=True)
    address = models.TextField(null=True)
    shipping_instructions = models.TextField(null=True)
    is_enabled_exchange = models.BooleanField(default=False)
    preferences = models.TextField(null=True)
    fb_profile_url = models.URLField(null=True)
    twitter_profile_url = models.URLField(null=True)
    website_url = models.URLField(null=True)
    wishlist_url = models.URLField(null=True)
    avatar = models.ImageField(
        upload_to=avatar_file_name, default='../static/img/avatar.jpg')

    user = models.OneToOneField(User)
    santee = models.OneToOneField(User, related_name='santa', null=True)

    def __str__(self):
        return self.user.username
