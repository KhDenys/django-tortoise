import pytest

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.test import override_settings

from .models import ModelA, ModelARel
from .serializers import serialize_model_a, serialize_model_a_rel


@pytest.mark.parametrize(
    'model', [
        LogEntry,
        Group,
        Permission,
        User,
        ContentType,
        Session,
        ModelA,
        ModelARel,
    ]
)
def test_check_if_model_is_monkey_patched(model):
    assert hasattr(model, 'abjects')


@pytest.mark.parametrize(
    'use_tz', [False, True]
)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_user_count(use_tz):
    with override_settings(USE_TZ=use_tz):
        sync_len = len(User.objects.all())
        async_len = len(await User.abjects.all())
        assert sync_len == async_len


@pytest.mark.parametrize(
    'use_tz', [False, True]
)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_model_a_creat_through_django(generate_a_as_dict, use_tz):
    with override_settings(USE_TZ=use_tz):
        a_dict = generate_a_as_dict()

        instance_a = ModelA.objects.create(**a_dict)

        instance_a_django = ModelA.objects.get(id=instance_a.id)
        instance_a_tortoise = await ModelA.abjects.get(id=instance_a.id)
        a_dict_django = serialize_model_a(instance_a_django)
        a_dict_tortoise = serialize_model_a(instance_a_tortoise)

        assert a_dict_django == a_dict_tortoise


@pytest.mark.parametrize(
    'use_tz', [False, True]
)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_model_a_creat_through_tortoise(generate_a_as_dict, use_tz):
    with override_settings(USE_TZ=use_tz):
        a_dict = generate_a_as_dict()

        instance_a = await ModelA.abjects.create(**a_dict)

        instance_a_django = ModelA.objects.get(id=instance_a.id)
        instance_a_tortoise = await ModelA.abjects.get(id=instance_a.id)
        a_dict_django = serialize_model_a(instance_a_django)
        a_dict_tortoise = serialize_model_a(instance_a_tortoise)

        assert a_dict_django == a_dict_tortoise


@pytest.mark.parametrize(
    'use_tz', [False, True]
)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_model_b_creat_through_django(generate_a_as_dict, use_tz):
    with override_settings(USE_TZ=use_tz):
        instance_a_rel = ModelARel.objects.create(
            one=ModelA.objects.create(**generate_a_as_dict()),
            foreign=ModelA.objects.create(**generate_a_as_dict())
        )
        instance_a_rel.many.add(ModelA.objects.create(**generate_a_as_dict()))

        instance_a_rel_django = ModelARel.objects.get(id=instance_a_rel.id)
        instance_a_rel_tortoise = await ModelARel.abjects.filter(
            id=instance_a_rel.id
        ).select_related(
            'one',
            'foreign',
        ).prefetch_related(
            'many',
        ).get()

        a_rel_dict_django = serialize_model_a_rel(instance_a_rel_django)
        a_rel_dict_tortoise = serialize_model_a_rel(instance_a_rel_tortoise)

        assert a_rel_dict_django == a_rel_dict_tortoise


@pytest.mark.parametrize(
    'use_tz', [False, True]
)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_model_b_creat_through_tortoise(generate_a_as_dict, use_tz):
    with override_settings(USE_TZ=use_tz):
        instance_a_rel = await ModelARel.abjects.create(
            one=(await ModelA.abjects.create(**generate_a_as_dict())),
            foreign=(await ModelA.abjects.create(**generate_a_as_dict()))
        )
        await instance_a_rel.many.add(await ModelA.abjects.create(**generate_a_as_dict()))

        instance_a_rel_django = ModelARel.objects.get(id=instance_a_rel.id)
        instance_a_rel_tortoise = await ModelARel.abjects.filter(
            id=instance_a_rel.id
        ).select_related(
            'one',
            'foreign',
        ).prefetch_related(
            'many',
        ).get()

        a_rel_dict_django = serialize_model_a_rel(instance_a_rel_django)
        a_rel_dict_tortoise = serialize_model_a_rel(instance_a_rel_tortoise)

        assert a_rel_dict_django == a_rel_dict_tortoise
