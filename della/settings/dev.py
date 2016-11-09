from .common import *

INVITE_CODE = 'HAHAHAHAHAHA'
SENDER_EMAIL = 'admin@secret.santa'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n$y%cmal2yps%^**#f=1s6f*5)s4xo6*ztddyr=c&3=&o!693w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
