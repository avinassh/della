#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # select settings according to environment.
    if os.environ.get('ON_HEROKU'):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "della.settings.heroku")
    else:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "della.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
