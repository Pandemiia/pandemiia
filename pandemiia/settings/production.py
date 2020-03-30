from .base import *

import dj_database_url

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Configure from DATABASE_URL
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
