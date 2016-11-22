from .common import *
from .secret import (DB_SETTINGS, SECRET_KEY, INVITE_CODE, SENDER_EMAIL,
                     ADMINS, SPARKPOST_API_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
    }
}

DATABASES['default'].update(DB_SETTINGS)

# SSL Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
