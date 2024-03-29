"""
Django settings for strategy_manager project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)
DEVEL = config("DEBUG", cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local apps
    'strategy',
    'celery_dynamic_schedule',
    'broker_manager'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'strategy_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'strategy_manager.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '{levelname}: {asctime}  module={module} filename={filename} pathname={pathname} lineno={lineno} '
                      'precess={process}  thread={thread} threadName={threadName}  msg={message} info={info}',
            'style': '{'
        },
    },
    'filters': {
        'system_log_filter': {
            '()': 'helpers.logger_handler.SystemLogFilter',
         },
    },
    'handlers': {
        'console': {
            'filters': ['system_log_filter'],
            'class': 'logging.StreamHandler',
            'formatter': 'base',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

RABBIT_HOST = config('RABBIT_HOST', default='localhost')
RABBIT_PORT = config('RABBIT_PORT', default='5672')
RABBIT_USERNAME = config('RABBIT_USERNAME', default='')
RABBIT_PASSWORD = config('RABBIT_PASSWORD', default='')

CELERY_BROKER_URL = f'amqp://{RABBIT_USERNAME}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}'
SHARED_TASK_TIME_LIMIT = config('SHARED_TASK_TIME_LIMIT', default=5, cast=int)

# task names
TRADINGVIEW_STRATEGY_CHECK_TASK = 'tradingview_strategy_check'
THIRD_PARTY_MANAGER_TASK = 'third_party_manager'
SEND_BROKER = "send_broker"

# websocket configs
TRADINGVIEW_WEBSOCKET_URL = config("TRADINGVIEW_WEBSOCKET_URL", default='')
CS_TOKEN = config('CS_TOKEN', default='')
QS_TOKEN = config('QS_TOKEN', default='')
AUTH_TOKEN = config('AUTH_TOKEN', default='')
TRADINGVIEW_USERNAME = config('TRADINGVIEW_USERNAME', default='')

# telegram config
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN', default="")
TELEGRAM_MODULE = config('TELEGRAM_MODULE', default='telegram_sender')
TELEGRAM_CHAT_ID_FOR_TRACK_PROBLEM = config('TELEGRAM_CHAT_ID_FOR_TRACK_PROBLEM', default="")

BINANCE_CONFIG = {
    "host": config("BINANCE_HOST", default=""),
    'api_key': config('BINANCE_API_KEY', default=""),
    'secret_key': config('BINANCE_SECRET_KEY', default=""),
    "new_order_endpoint_future": config("BINANCE_NEW_ORDER_ENDPOINT_FUTURE", default="/fapi/v1/order"),
    'position_information': config('BINANCE_POSITION_INFORMATION', default='/fapi/v2/positionRisk'),
    'change_leverage': config('BINANCE_CHANGE_LEVERAGE', default='/fapi/v1/leverage')
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
