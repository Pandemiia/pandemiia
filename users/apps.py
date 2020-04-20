from contextlib import suppress

from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = 'users'
    verbose_name = 'Users'

    def ready(self):
        with suppress(ImportError):
            from users import signals  # noqa: F401 pylint: disable=import-outside-toplevel
