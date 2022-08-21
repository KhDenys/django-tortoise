import pytest

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.test import override_settings

from .models import ModelA, ModelARel
from .serializers import serialize_model_a


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
async def test_creat_through_django(generate_a_as_dict, use_tz):
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
async def test_creat_through_tortoise(generate_a_as_dict, use_tz):
    with override_settings(USE_TZ=use_tz):
        a_dict = generate_a_as_dict()

        instance_a = await ModelA.abjects.create(**a_dict)

        instance_a_django = ModelA.objects.get(id=instance_a.id)
        instance_a_tortoise = await ModelA.abjects.get(id=instance_a.id)
        a_dict_django = serialize_model_a(instance_a_django)
        a_dict_tortoise = serialize_model_a(instance_a_tortoise)

        assert a_dict_django == a_dict_tortoise
