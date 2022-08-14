import pytest

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

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


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_user_count():
    sync_len = len(User.objects.all())
    async_len = len(await User.abjects.all())
    assert sync_len == async_len


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_creat_through_django(generate_a_as_dict):
    a_dict = generate_a_as_dict()

    instance_a = ModelA.objects.create(**a_dict)

    instance_a_django = ModelA.objects.get(id=instance_a.id)
    instance_a_tortoise = await ModelA.abjects.get(id=instance_a.id)

    assert serialize_model_a(instance_a_django) == serialize_model_a(instance_a_tortoise)
