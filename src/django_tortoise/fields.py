import datetime

from django.core.validators import validate_email, validate_slug, validate_unicode_slug, URLValidator
from django.utils.dateparse import parse_duration
from django.utils.ipv6 import clean_ipv6_address
from tortoise.fields.base import Field
from tortoise.fields.data import CharField
from tortoise.validators import validate_ipv46_address, MinValueValidator, MaxValueValidator


class DurationField(Field, datetime.timedelta):
    class _db_postgres:
        SQL_TYPE = 'INTERVAL'

    class _db_sqlite:
        SQL_TYPE = 'BIGINT'

    def to_python_value(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.timedelta):
            return value
        try:
            parsed = parse_duration(value)
        except ValueError:
            pass
        else:
            if parsed is not None:
                return parsed

    def to_db_value(self, value, instance):
        self.validate(value)

        if value is None:
            return None
        return (value.days * 86400000000) + (value.seconds * 1000000) + value.microseconds


class EmailField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 254)
        super().__init__(*args, **kwargs)
        self.validators.append(validate_email)


class GenericIPAddressField(Field):
    class _db_postgres:
        SQL_TYPE = 'INET'

    class _db_sqlite:
        SQL_TYPE = 'CHAR(39)'

    def __init__(self, protocol="both", unpack_ipv4=False, *args, **kwargs):
        self.unpack_ipv4 = unpack_ipv4
        self.protocol = protocol
        super().__init__(*args, **kwargs)
        self.validators.append(validate_ipv46_address)

    def to_python_value(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        if ":" in value:
            return clean_ipv6_address(value, self.unpack_ipv4)
        return value

    def to_db_value(self, value, instance):
        if value is None:
            return None
        if value and ":" in value:
            try:
                return clean_ipv6_address(value, self.unpack_ipv4)
            except ValueError:
                pass
        return str(value)


class SlugField(CharField, str):
    def __init__(self, allow_unicode=False, **kwargs):
        self.allow_unicode = allow_unicode

        kwargs.setdefault("max_length", 50)
        super().__init__(**kwargs)

        if allow_unicode:
            self.validators.append(validate_unicode_slug)
        else:
            self.validators.append(validate_slug)


class URLField(CharField, str):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 200)
        super().__init__(**kwargs)
        self.validators.append(URLValidator())


class PositiveBigIntegerField(Field, int):
    class _db_postgres:
        SQL_TYPE = 'BIGINT'

    class _db_sqlite:
        SQL_TYPE = 'BIGINT UNSIGNED'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators += [
            MinValueValidator(0),
            MaxValueValidator(9223372036854775807)
        ]


class PositiveIntegerField(Field, int):
    class _db_postgres:
        SQL_TYPE = 'INTEGER'

    class _db_sqlite:
        SQL_TYPE = 'INTEGER UNSIGNED'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators += [
            MinValueValidator(0),
            MaxValueValidator(2147483647)
        ]


class PositiveSmallIntegerField(Field, int):
    class _db_postgres:
        SQL_TYPE = 'SMALLINT'

    class _db_sqlite:
        SQL_TYPE = 'SMALLINT UNSIGNED'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators += [
            MinValueValidator(0),
            MaxValueValidator(32767)
        ]
