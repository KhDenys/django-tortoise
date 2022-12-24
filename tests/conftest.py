import asyncio
import datetime
import importlib.util
import json
import sys

import django
import pytest

from pathlib import Path

from faker import Faker

from django.conf import settings
from django.core.handlers.asgi import ASGIHandler
from tortoise import Tortoise

from django_tortoise.models import tortoise_setup, __init

django_tortoise_name = 'django_tortoise'
django_tortoise_path = Path(__file__).resolve().parent.parent / 'src' / 'django_tortoise' / '__init__.py'

spec = importlib.util.spec_from_file_location(django_tortoise_name, django_tortoise_path)
module = importlib.util.module_from_spec(spec)
sys.modules[django_tortoise_name] = module
spec.loader.exec_module(module)


@pytest.fixture(scope='session')
def event_loop():

    loop = asyncio.get_event_loop()

    ASGIHandler()

    from django.apps import apps
    tortoise_setup(apps)

    loop.run_until_complete(__init())

    yield loop

    loop.run_until_complete(Tortoise.close_connections())
    loop.close()


@pytest.fixture(scope='session')
def django_db_setup():
    if django.VERSION[:2] >= (4, 1):
        settings.DATABASES['default'].update({
            'TIME_ZONE': 'Europe/Kiev',
            'CONN_HEALTH_CHECKS': False,
            'CONN_MAX_AGE': 0,
            'OPTIONS': {},
            'AUTOCOMMIT': True
        })


@pytest.fixture(scope='session')
def generate_a_as_dict():
    fake = Faker()

    return lambda: {
        'binary': fake.pystr().encode(),
        'boolean': fake.pybool(),
        'char': fake.pystr(),
        'decimal': fake.pydecimal(left_digits=2, right_digits=8),
        'duration': datetime.timedelta(minutes=fake.pyint(max_value=2147483647)),
        'float': fake.pyfloat(),
        'ip': fake.ipv4(),
        'integer': fake.pyint(min_value=-2147483648, max_value=2147483647),
        'small_int': fake.pyint(min_value=-32768, max_value=32767),
        'json': json.loads(
            fake.json(
                data_columns=[('Name', 'name'), ('Points', 'pyint', {'min_value': 50, 'max_value': 100})],
                num_rows=1
            )
        ),
        'positive_big_int': fake.pyint(max_value=9223372036854775807),
        'positive_int':  fake.pyint(max_value=2147483647),
        'positive_small_int':  fake.pyint(max_value=32767),
        'slug': fake.slug(),
        'text': fake.pystr(min_chars=20, max_chars=1_000),
        'url': fake.url(),
        'uuid': fake.uuid4(),
    }
