from django.template.loader import render_to_string
from django.urls import reverse

from della.email_service import send_email

from .models import UserProfile
from . import activation_service


def create_user_profile(user):
    UserProfile.objects.create(user=user, is_enabled_exchange=False)


def activate_user(user):
    if user.is_active:
        return True
    user.is_active = True
    user.save()
    return True


def enable_for_exchange(user):
    if user.userprofile.is_enabled_exchange:
        return True
    user.userprofile.is_enabled_exchange = True
    user.userprofile.save()
    return True


def send_activation_email(request, user):
    message_template = 'user_manager/account_activation_email.html'
    subject_temaplte = 'user_manager/account_activation_subject.txt'
    code = activation_service.generate_key(user)
    path_params = {'username': user.username, 'code': code}
    activation_url = request.build_absolute_uri(reverse(
        'user_manager:activate-user', kwargs=path_params))
    context = {'url': activation_url, 'username': user.username}
    message = render_to_string(template_name=message_template, context=context)
    subject = render_to_string(template_name=subject_temaplte)
    send_email(subject=subject, message=message, recipient_list=[user.email])
