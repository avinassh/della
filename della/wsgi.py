"""
WSGI config for nightreads project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

if os.environ.get('ON_HEROKU'):
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "della.settings.heroku")
    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "della.settings.production")
    application = get_wsgi_application()
