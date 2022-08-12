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
