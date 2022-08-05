from django.db import models
from tortoise import fields

from .fields import (
    DurationField,
    GenericIPAddressField,
    SlugField,
    URLField,
    PositiveBigIntegerField,
    PositiveIntegerField,
    PositiveSmallIntegerField
)


BASE_KWARGS = {
    'null': 'null',
    'db_column': 'source_field',
    'default': 'default',
    'primary_key': 'pk',
    'db_index': 'index',
    'unique': 'unique',
    'validators': 'validators'
}


def __get_base_field_kwargs(django_field):
    return {
        tortoise_option: getattr(django_field, django_option, None)
        for django_option, tortoise_option in BASE_KWARGS.items()
    }


def __get_auto_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.IntField(**base_kwargs, pk=True)


def __get_big_auto_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.BigIntField(**base_kwargs, pk=True)


def __get_big_integer_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.BigIntField(**base_kwargs)


def __get_binary_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.BinaryField(**base_kwargs)


def __get_boolean_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.BooleanField(**base_kwargs)


def __get_char_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    max_length = django_field.max_length
    return fields.CharField(**base_kwargs, max_length=max_length)


def __get_date_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    auto_now, auto_now_add = django_field.auto_now, django_field.auto_now_add
    return fields.DateField(**base_kwargs, auto_now=auto_now, auto_now_add=auto_now_add)


def __get_date_time_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    auto_now, auto_now_add = django_field.auto_now, django_field.auto_now_add
    return fields.DatetimeField(**base_kwargs, auto_now=auto_now, auto_now_add=auto_now_add)


def __get_decimal_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    max_digits, decimal_places = django_field.max_digits, django_field.decimal_places
    return fields.DecimalField(**base_kwargs, max_digits=max_digits, decimal_places=decimal_places)


def __get_duration_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return DurationField(**base_kwargs)


def __get_email_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    max_length = django_field.max_length
    return fields.BooleanField(**base_kwargs,  max_length=max_length)


def __get_file_field(django_field):
    raise NotImplementedError('FileField is not implemented')


def __get_file_path_field(django_field):
    raise NotImplementedError('FilePathField is not implemented')


def __get_float_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.FloatField(**base_kwargs)


def __get_generic_ip_address_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    protocol, unpack_ipv4 = django_field.protocol, django_field.unpack_ipv4
    return GenericIPAddressField(**base_kwargs, protocol=protocol, unpack_ipv4=unpack_ipv4)


def __get_image_field(django_field):
    raise NotImplementedError('ImageField is not implemented')


def __get_integer_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.IntField(**base_kwargs)


def __get_json_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    encoder, decoder = django_field.encoder, django_field.decoder
    return fields.JSONField(**base_kwargs, encoder=encoder, decoder=decoder)


def __get_positive_big_integer_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return PositiveBigIntegerField(**base_kwargs)


def __get_positive_integer_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return PositiveIntegerField(**base_kwargs)


def __get_positive_small_integer_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return PositiveSmallIntegerField(**base_kwargs)


def __get_slug_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    max_length = django_field.max_length
    allow_unicode = django_field.allow_unicode
    return SlugField(**base_kwargs, max_length=max_length, allow_unicode=allow_unicode)


def __get_small_auto_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.SmallIntField(**base_kwargs, pk=True)


def __get_small_integer_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.SmallIntField(**base_kwargs)


def __get_text_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.TextField(**base_kwargs)


def __get_time_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    auto_now, auto_now_add = django_field.auto_now, django_field.auto_now_add
    return fields.TimeField(**base_kwargs, auto_now=auto_now, auto_now_add=auto_now_add)


def __get_url_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    max_length = django_field.max_length
    return URLField(**base_kwargs, max_length=max_length)


def __get_uuid_field(django_field):
    base_kwargs = __get_base_field_kwargs(django_field)
    return fields.UUIDField(**base_kwargs)


ON_DELETE = {
        models.CASCADE: fields.CASCADE,
        models.SET_NULL: fields.SET_NULL,
        models.SET_DEFAULT: fields.SET_DEFAULT
    }


def __get_foreign_key_field(django_field):
    to = django_field.to
    if isinstance(to, str):
        if '.' in to:
            to = to.split('.')[-1]
    else:
        to = to.__name__

    model_name = f'{to}Tortoise'
    related_name = django_field.related_name
    on_delete = ON_DELETE[django_field.on_delete]

    return fields.ForeignKeyField(model_name=model_name, related_name=related_name, on_delete=on_delete)


def __get_one_to_one_field(django_field):
    to = django_field.to
    if isinstance(to, str):
        if '.' in to:
            to = to.split('.')[-1]
    else:
        to = to.__name__

    model_name = f'{to}Tortoise'
    related_name = django_field.related_name
    on_delete = ON_DELETE[django_field.on_delete]

    return fields.OneToOneField(model_name=model_name, related_name=related_name, on_delete=on_delete)


def __get_many_to_many_field(django_field):
    to = django_field.to
    if isinstance(to, str):
        if '.' in to:
            to = to.split('.')[-1]
    else:
        to = to.__name__

    model_name = f'{to}Tortoise'
    related_name = django_field.related_name
    on_delete = ON_DELETE[django_field.on_delete]

    through = django_field.through
    if isinstance(through, str):
        if '.' in through:
            through = through.split('.')[-1]
    else:
        through = through.__name__

    through = f'{through}Tortoise'

    forward_key = None
    backward_key = None
    through_fields = django_field.through_fields
    if through_fields:
        backward_key, forward_key = through_fields

    return fields.ManyToManyField(
        model_name=model_name,
        related_name=related_name,
        through=through,
        forward_key=forward_key,
        backward_key=backward_key,
        on_delete=on_delete
    )


# # reverse relationship fields
# def __get_many_to_one_rel(django_field):



DJANGO_TORTOISE_FIELD_MAPPING = {
    # data fields
    models.AutoField: __get_auto_field,
    models.BigAutoField: __get_big_auto_field,
    models.BigIntegerField: __get_big_integer_field,
    models.BinaryField: __get_binary_field,
    models.BooleanField: __get_boolean_field,
    models.CharField: __get_char_field,
    models.DateField: __get_date_field,
    models.DateTimeField: __get_date_time_field,
    models.DecimalField: __get_decimal_field,
    models.DurationField: __get_duration_field,
    models.EmailField: __get_email_field,
    models.FileField: __get_file_field,
    models.FilePathField: __get_file_path_field,
    models.FloatField: __get_float_field,
    models.GenericIPAddressField: __get_generic_ip_address_field,
    models.ImageField: __get_image_field,
    models.IntegerField: __get_integer_field,
    models.JSONField: __get_json_field,
    models.PositiveBigIntegerField: __get_positive_big_integer_field,
    models.PositiveIntegerField: __get_positive_integer_field,
    models.PositiveSmallIntegerField: __get_positive_small_integer_field,
    models.SlugField: __get_slug_field,
    models.SmallAutoField: __get_small_auto_field,
    models.SmallIntegerField: __get_small_integer_field,
    models.TextField: __get_text_field,
    models.TimeField: __get_time_field,
    models.URLField: __get_url_field,
    models.UUIDField: __get_uuid_field,

    # relationship fields
    models.ForeignKey: __get_foreign_key_field,
    models.OneToOneField: __get_one_to_one_field,
    models.ManyToManyField: __get_many_to_many_field,

    # reverse relationship fields
    # models.ManyToOneRel: __get_many_to_one_rel,
}
