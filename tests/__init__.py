# -*- coding: utf-8 -*-

"""Unit test package for django-tortoise."""

# Having tests in a separate folder is a safe choice
# You can have them mixed in the src but at some point you will get
# problems with test discovery activating lazy objects and other import time
# headaches. And if you fail to filter test during packaging you will get
# similar problems in production.
