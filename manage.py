#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # use local_settings if exist
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'pandemiia/settings/local_settings.py')):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pandemiia.settings.local_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pandemiia.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
