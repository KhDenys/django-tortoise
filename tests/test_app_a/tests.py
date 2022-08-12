import pytest

from .models import ModelA, ModelARel


@pytest.mark.asyncio
@pytest.mark.django_db
@pytest.mark.parametrize(
    'model', [
        ModelA,
        ModelARel
    ]
)
async def test(model):
    assert hasattr(model, 'abjects')
