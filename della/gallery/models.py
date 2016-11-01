from django.db import models
from django.contrib.auth.models import User

from della.utils import TimeStampMixin


class Image(TimeStampMixin):
    file = models.ImageField(upload_to='images/%Y/%m/%d')
    added_by = models.ForeignKey(User)
