from .models import UserProfile


def send_activation_email(user):
    pass


def create_user_profile(user):
    UserProfile.objects.create(user=user, is_enabled_exchange=False)


def activate_user(user):
    if user.is_active:
        return True
    user.is_active = True
    user.save()
    return True
