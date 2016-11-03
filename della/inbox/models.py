from django.db import models
from django.contrib.auth.models import User

from della.utils import TimeStampMixin


class Thread(TimeStampMixin):
    """
    `is_sneaky` flag will be used when the message thread is between santa and
    santee. If `is_sneaky` is set to `True` then `santa` shouldn't be null.

    `participant_1.id` will be always less than `participant_2.id`
    """
    is_sneaky = models.BooleanField(default=False)

    participant_1 = models.ForeignKey(
        User, related_name='participant_1_threads')
    participant_2 = models.ForeignKey(
        User, related_name='participant_2_threads')
    santa = models.ForeignKey(User, null=True, related_name='santa_threads')


class Message(TimeStampMixin):
    text = models.TextField()

    sent_by = models.ForeignKey(User)
    thread = models.ForeignKey(Thread, related_name='messages')
