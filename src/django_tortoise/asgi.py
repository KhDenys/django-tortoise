from django.core.handlers.asgi import ASGIHandler

from .models import tortoise_setup, tortoise_init


def get_boosted_asgi_application(app):
    if not isinstance(app, ASGIHandler):
        raise TypeError('Tortoise ORM must be used in ASGI mode')

    from django.apps import apps
    tortoise_setup(apps)
    tortoise_init()

    return app
