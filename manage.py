#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import os
import sys

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("PIL.Image").setLevel(logging.WARNING)
logging.disable(logging.NOTSET)
logging.getLogger('environ').setLevel(logging.INFO)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
