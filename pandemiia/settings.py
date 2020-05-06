import os
import environ


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 2  # (/a/myfile.py - 2 = /)

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'CHANGEME!!!j&3a)=&eflya=2@hmg!tsa(mb6h3lcno4#p9oct$o1&@l75-%2',),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_STATIC_ROOT=(str, str(BASE_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(BASE_DIR('media'))),
    DJANGO_DATABASE_URL=(str, 'sqlite:///pandemiia'),
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),
    DJANGO_CELERY_BROKER_URL=(str, 'redis://localhost:6379/0'),
    DJANGO_CELERY_BACKEND=(str, 'redis://localhost:6379/0'),
    DJANGO_CELERY_ALWAYS_EAGER=(bool, False),
    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_TEST_RUN=(bool, False),
    DJANGO_HEALTH_CHECK_BODY=(str, 'Success'),
    DJANGO_SITE_ID=(int, 1)
)
environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG')

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

ADMINS = tuple(
    [tuple(admins.split(':')) for admins in env.list('DJANGO_ADMINS')],
)

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL'),
}

# Django Email Server
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-backend
# ------------------------------------------------------------------------------
EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')
EMAIL_BACKEND = EMAIL_URL['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER', '')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT', '')
EMAIL_USE_SSL = 'EMAIL_USE_SSL' in EMAIL_URL
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in EMAIL_URL
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH', '')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL')


# SECURE_SSL_REDIRECT = False
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    'django_extensions',
    'drf_yasg',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django_filters',

    # local apps 
    'medsupport',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'pandemiia.urls'

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.path('templates')),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pandemiia.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')

MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

STATICFILES_DIRS = (
    str(BASE_DIR.path('static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Password validation -- not needed yet
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Django Auth
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTH_USER_MODEL = 'users.User'
# LOGIN_URL = 'users:auth:login'
LOGIN_REDIRECT_URL = '/'

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False

# django-rest-auth
# https://django-rest-auth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
LOGOUT_ON_PASSWORD_CHANGE = False
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'users.serializers.TokenSerializer',
    'PASSWORD_RESET_SERIALIZER': 'users.serializers.PasswordResetSerializer'
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'uk'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# DRF yasg redirection fix
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}

