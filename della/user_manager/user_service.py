from .models import UserProfile


def send_activation_email(user):
    pass


def create_user_profile(user):
    UserProfile.objects.create(user=user, is_enabled_exchange=False)
