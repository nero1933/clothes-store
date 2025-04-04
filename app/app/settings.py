"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 0)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # libs
    'rest_framework',
    'rest_framework_simplejwt',
    'debug_toolbar',
    'drf_spectacular',
    'django_filters',
    'phonenumber_field',
    'django_celery_beat',
    'corsheaders',

    # apps
    'ecommerce.apps.EcommerceConfig',
]

MIDDLEWARE = [
    # libs
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django REST Framework
# https://www.django-rest-framework.org

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'COERCE_DECIMAL_TO_STRING': False,
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 100

    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# django-redis
# https://pypi.org/project/django-redis/

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# drf-spectacular
# https://drf-spectacular.readthedocs.io/en/latest/

SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commence clothes-store',
    'DESCRIPTION': 'My pet project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/static/'
MEDIA_URL = 'static/media/'

STATIC_ROOT = 'vol/web/static/'
MEDIA_ROOT = 'vol/web/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'ecommerce.UserProfile'

# Sendgrid api (SMTP API)
# https://docs.sendgrid.com/for-developers/sending-email/django

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Stripe
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", 0)
STRIPE_DEVICE_NAME = os.environ.get("STRIPE_DEVICE_NAME", 0)
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", 0)

# Coverage
# https://docs.djangoproject.com/en/4.2/topics/testing/advanced/#measuring-code-coverage
# Integration with coverage.py

COVERAGE_MODULE_EXCLUDES = [
    'tests*',
    'admin*',
    'settings*',
    'urls*',
    'wsgi*',
    '*/migrations/*',
]

COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage'

# Celery
# https://docs.celeryq.dev/en/stable/

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TIMEZONE = 'Europe/Kyiv'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# CORS

# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Адрес вашего фронтенда
    # "http://localhost:8000",  # Адрес вашего API
]

# CORS_ORIGIN_WHITELIST = [
#      'http://localhost:3000'
# ]

# Logging

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'}
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}



# Custom variables

FRONTEND_URL = os.environ.get('FRONTEND_URL')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# -----------------
# USER_CONFIRMATION

USER_CONFIRMATION_KEY_TEMPLATE = os.environ.get('USER_CONFIRMATION_KEY_TEMPLATE')
USER_CONFIRMATION_KEY_TIMEOUT = int(os.environ.get('USER_CONFIRMATION_KEY_TIMEOUT', 0))

USER_CONFIRMATION_COUNTER_TEMPLATE = os.environ.get('USER_CONFIRMATION_COUNTER_TEMPLATE')
USER_CONFIRMATION_COUNTER_TIMEOUT = int(os.environ.get('USER_CONFIRMATION_COUNTER_TIMEOUT', 0))

USER_CONFIRMATION_MAX_ATTEMPTS = int(os.environ.get('USER_CONFIRMATION_MAX_ATTEMPTS', 0))

# --------------
# RESET_PASSWORD

RESET_PASSWORD_KEY_TEMPLATE = os.environ.get('RESET_PASSWORD_KEY_TEMPLATE')
RESET_PASSWORD_KEY_TIMEOUT = int(os.environ.get('RESET_PASSWORD_KEY_TIMEOUT', 0))

RESET_PASSWORD_COUNTER_TEMPLATE = os.environ.get('RESET_PASSWORD_COUNTER_TEMPLATE')
RESET_PASSWORD_COUNTER_TIMEOUT = int(os.environ.get('RESET_PASSWORD_COUNTER_TIMEOUT', 0))

RESET_PASSWORD_MAX_ATTEMPTS = int(os.environ.get('RESET_PASSWORD_MAX_ATTEMPTS', 0))



if DEBUG:
    # `debug` is only True in templates if the visitor IP is in INTERNAL_IPS.
    INTERNAL_IPS = type("c", (), {"__contains__": lambda *a: True})()

# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
