from django.utils import timezone
from django.utils.timezone import get_default_timezone


def serialize_model_a(instance):
    return {
        'id': instance.id,
        'binary': instance.binary,
        'boolean': instance.boolean,
        'char': instance.char,
        'date': instance.date,
        'datetime': instance.datetime,
        'decimal': instance.decimal,
        'duration': instance.duration,
        'float': instance.float,
        'ip': instance.ip,
        'integer': instance.integer,
        'small_int': instance.small_int,
        'json': instance.json,
        'positive_big_int': instance.positive_big_int,
        'positive_int': instance.positive_int,
        'positive_small_int': instance.positive_small_int,
        'slug': instance.slug,
        'text': instance.text,
        'time': instance.time,
        'url': instance.url,
        'uuid': instance.uuid,
    }
