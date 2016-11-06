from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        html_message=message.replace('\n', '<br />'),
        from_email=settings.SENDER_EMAIL,
        recipient_list=recipient_list,
    )
