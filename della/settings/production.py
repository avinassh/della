from .common import *
from .secret import DB_SETTINGS, SECRET_KEY, INVITE_CODE, SENDER_EMAIL, ADMINS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
    }
}

DATABASES['default'].update(DB_SETTINGS)
