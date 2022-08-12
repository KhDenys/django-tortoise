import importlib.util
import sys

from pathlib import Path

from django.core.handlers.asgi import ASGIHandler

django_tortoise_name = 'django_tortoise'
django_tortoise_path = Path(__file__).resolve().parent.parent / 'src' / 'django_tortoise' / '__init__.py'

spec = importlib.util.spec_from_file_location(django_tortoise_name, django_tortoise_path)
module = importlib.util.module_from_spec(spec)
sys.modules[django_tortoise_name] = module
spec.loader.exec_module(module)

from django_tortoise import get_boosted_asgi_application


def pytest_sessionstart(session):
    # monkey patch django orm
    get_boosted_asgi_application(ASGIHandler())
