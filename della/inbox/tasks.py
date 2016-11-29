from urllib.parse import urljoin
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from background_task import background

from della.email_service import send_email
from .models import Message
from . import inbox_service


@background(queue=settings.INBOX_EMAIL_NOTIFICATION_QUEUE)
def send_email_notification(message_id, base_site_url):
    message_template = 'inbox/message_notification_email.html'
    message = Message.objects.select_related('thread').get(pk=message_id)
    thread = message.thread
    sender = message.sent_by
    recipient = inbox_service.get_recipient(thread=thread, sender=sender)
    subject, sender_name, url_path = _get_email_context(
        thread=thread, message=message, recipient=recipient)
    context = {
        'recipient': recipient.username,
        'sender': sender_name,
        'message': message.text,
        'url': urljoin(base_site_url, url_path)
    }
    m = render_to_string(template_name=message_template, context=context)
    send_email(subject=subject, message=m, recipient_list=[recipient.email])


def _get_email_context(thread, message, recipient):
    if thread.is_sneaky:
        return _get_email_context_sneaky(thread, message, recipient)
    sender_name = message.sent_by.username
    subject = 'You received a new message from {}'.format(
        message.sent_by.username)
    url_path = reverse(
        'inbox:thread-detail', kwargs={'recipient': message.sent_by})
    return subject, sender_name, url_path


def _get_email_context_sneaky(thread, message, recipient):
    sender_name = message.sent_by.username
    url_path = reverse('inbox:santee-detail')
    if thread.santa == message.sent_by:
        sender_name = 'your Santa'
        url_path = reverse('inbox:santa-detail')
    subject = 'You received a new *sneaky* message from {}'.format(sender_name)
    return subject, sender_name, url_path
