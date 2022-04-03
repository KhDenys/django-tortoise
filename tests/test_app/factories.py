# coding=utf-8
import factory
import faker
from django.contrib.auth import get_user_model

from . import models

fake = faker.Faker()


class UserFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Sequence(lambda n: fake.user_name() + str(n))
    is_staff = False
    is_active = True

    class Meta:
        model = get_user_model()


class NamedModelFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = models.NamedModel
