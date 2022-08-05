import signal


from django.conf import settings
from tortoise import models, Tortoise, run_async

from .mapping import DJANGO_TORTOISE_FIELD_MAPPING


SYMBIOTIC_MODELS = {}
TORTOISE_MODELS = {}


class _SymbioticModel:
    __slots__ = ('django_model', 'tortoise_model')

    def __init__(self, django_model, tortoise_model):
        self.django_model = django_model
        self.tortoise_model = tortoise_model


def tortoise_setup(apps):
    for app_models in apps.all_models.values():
        for model_name, django_model in app_models.items():
            tortoise_model = generate_tortoise_model(django_model)
            TORTOISE_MODELS[model_name] = tortoise_model
            setattr(django_model, 'abject', tortoise_model)  # the main magic

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
        tortoise_field = DJANGO_TORTOISE_FIELD_MAPPING[field_type](django_field)
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
            }
        },
        modules={'models': ['django_tortoise.models']}
    )


def __get_db_conf():
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

    elif engine == 'django.db.backends.sqlite3':
        tortoise_db_conf = {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": django_db_conf['NAME']},
        }

    else:
        raise NotImplementedError('Given database backend is not supported')

    return tortoise_db_conf


def register_tortoise_shutdown():
    for sig_num in (signal.SIGBREAK, signal.SIGHUP, signal.SIGINT, signal.SIGKILL, signal.SIGSEGV, signal.SIGTERM):
        signal.signal(sig_num, __shutdown_handler)


def __shutdown_handler(signum, frame):
    run_async(Tortoise.close_connections())


for model_name, tortoise_model in TORTOISE_MODELS.items():
    locals()[model_name] = tortoise_model
