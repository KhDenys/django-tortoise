# coding=utf-8

from django.conf import settings

# This is an example
DJANGO_TORTOISE_SECRET = settings.SECRET_KEY[::4]
