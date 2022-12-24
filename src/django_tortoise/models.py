import asyncio
import signal
import sys

from django.conf import settings
from tortoise import models, Tortoise

from .mapping import DJANGO_TORTOISE_FIELD_MAPPING


SYMBIOTIC_MODELS = {}
__models__ = list()
DB_BACKEND = None


class _SymbioticModel:
    __slots__ = ('django_model', 'tortoise_model')

    def __init__(self, django_model, tortoise_model):
        self.django_model = django_model
        self.tortoise_model = tortoise_model


def tortoise_setup(apps):
    for app_models in apps.all_models.values():
        for model_name, django_model in app_models.items():
            tortoise_model = generate_tortoise_model(django_model)
            __models__.append(tortoise_model)
            setattr(django_model, 'abjects', tortoise_model)  # the main magic

            SYMBIOTIC_MODELS[model_name] = _SymbioticModel(django_model, tortoise_model)


def generate_tortoise_model(django_model):
    model_name = django_model.__name__
    tortoise_fields = get_tortoise_fields(django_model)
    tortoise_meta_class = get_tortoise_meta_class(django_model)

    tortoise_model_name = f'{model_name}Tortoise'

    tortoise_model = type(
        tortoise_model_name,
        (
            models.Model,
        ),
        {
            'Meta': tortoise_meta_class,
            **tortoise_fields
        }
    )

    return tortoise_model


def get_tortoise_fields(django_model):

    tortoise_fields = {}
    for django_field in django_model._meta.get_fields(include_hidden=False):
        field_type = type(django_field)
        try:
            tortoise_field = DJANGO_TORTOISE_FIELD_MAPPING[field_type](django_field)
        except KeyError:
            # skip reverse related fields
            continue

        tortoise_fields[django_field.name] = tortoise_field

    return tortoise_fields


def get_tortoise_meta_class(django_model):
    meta = django_model._meta

    attribute_dict = {
        'abstract': meta.abstract,
        'table': meta.db_table,
        'schema': meta.db_tablespace,
        'ordering': meta.ordering
    }

    class_tortoise_meta = type(
        'Meta',
        tuple(),
        attribute_dict
    )

    return class_tortoise_meta


def tortoise_init():
    run_async(__init())
    register_tortoise_shutdown()


async def __init():
    db_conf = __get_db_conf()

    # support default db only
    await Tortoise.init(
        config={
            'connections': {
                'default': db_conf
            },
            'apps': {
                'django_tortoise': {
                    'models': ['django_tortoise.models'],
                    'default_connection': 'default'
                }
            }
        },
        use_tz=settings.USE_TZ,
        timezone=settings.TIME_ZONE
    )


def __get_db_conf():
    global DB_BACKEND

    # support default db only
    django_db_conf = settings.DATABASES['default']
    engine = django_db_conf['ENGINE']

    if engine == 'django.db.backends.postgresql':
        tortoise_db_conf = {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': django_db_conf['HOST'],
                'port': django_db_conf['PORT'],
                'user': django_db_conf['USER'],
                'password': django_db_conf['PASSWORD'],
                'database': django_db_conf['NAME'],
            }
        }

        DB_BACKEND = 'postgresql'

    elif engine == 'django.db.backends.sqlite3':
        tortoise_db_conf = {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": django_db_conf['NAME']},
        }

        DB_BACKEND = 'sqlite3'

    else:
        raise NotImplementedError('Given database backend is not supported')

    return tortoise_db_conf


def register_tortoise_shutdown():
    for signame in [x for x in dir(signal) if x.startswith("SIG")]:
        try:
            signum = getattr(signal, signame)
            signal.signal(signum, __shutdown_handler)
        except (OSError, RuntimeError, ValueError):
            pass


def __shutdown_handler(signum, _):
    run_async(Tortoise.close_connections())
    sys.exit(signum)


def run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        loop.create_task(coro)
    else:
        asyncio.run(coro)
