# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import logging
import os
from pathlib import Path

import environ

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)

logging.debug("Settings loading: %s" % __file__)

BASE_DIR = Path(__file__).parents[0]

environ.Env.read_env(str(Path(__file__).with_suffix('.env')))
env = environ.Env()

DEBUG = True

SECRET_KEY = env('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {}

if "DATABASE_URL" in os.environ:  # pragma: no cover
    DATABASES['default'] = env.db()
    DATABASES['default']['TEST'] = {'NAME': env("DATABASE_TEST_NAME", default=None)}
    DATABASES['default']['OPTIONS'] = {
        'options': '-c search_path=gis,public,pg_catalog',
        'sslmode': 'require',
    }
else:
    DATABASES['default'] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        'TEST': {
            "NAME": ":memory:",
        }
    }

logging.debug("DATABASES: %s", DATABASES['default']['NAME'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_tortoise.apps.DjangoTortoiseConfig",
    "tests.test_app",
]

ROOT_URLCONF = 'tests.urls'

TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/topics/templates/#django.template.backends.django.DjangoTemplates
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    # Setting this to True will disable for eg. preexisting Celery loggers
    'disable_existing_loggers': False,
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)-7s %(thread)-5d %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'short',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django.template': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.security.DisallowedHost': {
            'handlers': [],
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'factory.generate': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'factory.containers': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
}
