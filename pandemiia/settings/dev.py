from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

SECRET_KEY = "NOT_PRODUCTION_KEY"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, '../static')

