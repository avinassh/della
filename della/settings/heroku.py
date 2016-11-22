import dj_database_url
import os

from .common import *

SECRET_KEY = os.environ['SECRET_KEY']
INVITE_CODE = os.environ['INVITE_CODE']

# Sparkpost settings
SPARKPOST_API_KEY = os.environ['SPARKPOST_API_KEY']
SENDER_EMAIL = os.environ['SENDER_EMAIL']

DEBUG = False
ALLOWED_HOSTS = ['*']

# define Middlewares again with proper ordering for Whitenoise

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {}
DATABASES['default'] = {}
DATABASES['default'].update(db_from_env)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
