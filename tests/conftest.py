import datetime
import importlib.util
import json
import sys

import pytest

from pathlib import Path

from faker import Faker

from django.conf import settings
from django.core.handlers.asgi import ASGIHandler
from tortoise import Tortoise

django_tortoise_name = 'django_tortoise'
django_tortoise_path = Path(__file__).resolve().parent.parent / 'src' / 'django_tortoise' / '__init__.py'

spec = importlib.util.spec_from_file_location(django_tortoise_name, django_tortoise_path)
module = importlib.util.module_from_spec(spec)
sys.modules[django_tortoise_name] = module
spec.loader.exec_module(module)

from django_tortoise import get_boosted_asgi_application, run_async


def pytest_sessionstart(session):
    # monkey patch django orm
    get_boosted_asgi_application(ASGIHandler())


def pytest_sessionfinish(session, exitstatus):
    # manually close all connections to prevent tests hangs
    run_async(Tortoise.close_connections())


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(__file__).resolve().parent / 'db.sqlite3',
    }


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
        'integer': fake.pyint(min_value=-9223372036854775808, max_value=9223372036854775807),
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
