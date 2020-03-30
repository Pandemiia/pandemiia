from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

SECRET_KEY = "6%ls*13kzfwr##^&o52o=qkjb+qq^womb-skd)qa!5w-u)x4mh"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, '../static')

