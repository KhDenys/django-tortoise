def serialize_model_a(instance):
    return {
        'id': instance.id,
        'binary': bytes(instance.binary),
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


def serialize_model_a_rel(instance):
    return {
        'id': instance.id,
        'one': serialize_model_a(instance.one),
        'foreign': serialize_model_a(instance.foreign),
        'many': [
            serialize_model_a(instance_a)
            for instance_a in (instance.many if hasattr(instance._meta, 'app') else instance.many.all())
        ],
    }
