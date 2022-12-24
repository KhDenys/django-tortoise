import datetime
import warnings

import django
from django.conf import settings
from django.core.validators import validate_email, validate_slug, validate_unicode_slug, URLValidator
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time, parse_duration
from django.utils.duration import duration_microseconds, duration_string
from django.utils.ipv6 import clean_ipv6_address
from tortoise.fields.base import Field
from tortoise.fields.data import (
    CharField,
    DateField as TortoiseDateField,
    DatetimeField as TortoiseDateTimeField,
)
from tortoise.validators import validate_ipv46_address, MinValueValidator, MaxValueValidator


class BinaryField(Field, memoryview):
    indexable = False
    SQL_TYPE = "BLOB"

    class _db_postgres:
        SQL_TYPE = "BYTEA"


class DateField(TortoiseDateField):
    def __init__(self, auto_now, auto_now_add, **kwargs):
        # Do not check combination of auto_now, auto_now_add, and default
        # since it has been done by Django
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_python_value(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            if settings.USE_TZ and timezone.is_aware(value):
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_naive(value, default_timezone)
            value = value.date()
            self.validate(value)
            return value
        if isinstance(value, datetime.date):
            self.validate(value)
            return value

        parsed = parse_date(value)
        if parsed is not None:
            self.validate(parsed)
            return parsed

        raise ValueError(f'Bad value: {value}')

    def to_db_value(self, value, instance):
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = datetime.date.today()
            setattr(instance, self.model_field_name, value)
            self.validate(value)
            return value
        if value is not None:
            value = self.to_python_value(value)
            return value


class DateTimeField(TortoiseDateTimeField):
    def to_python_value(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            if settings.USE_TZ:
                from .models import DB_BACKEND
                if DB_BACKEND == 'sqlite3':
                    pass
                elif DB_BACKEND == 'postgresql':

                    if django.VERSION[:2] >= (4, 1):
                        default_timezone = timezone.get_default_timezone()
                    else:
                        default_timezone = timezone.utc

                    value = value.astimezone(default_timezone)
            else:
                if timezone.is_aware(value):
                    value = timezone.make_naive(value)
            self.validate(value)
            return value
        if isinstance(value, datetime.date):
            value = datetime.datetime(value.year, value.month, value.day)
            if settings.USE_TZ:
                # For backwards compatibility, interpret naive datetimes in
                # local time. This won't work during DST change, but we can't
                # do much about it, so we let the exceptions percolate up the
                # call stack.
                warnings.warn(
                    "DateTimeField %s.%s received a naive datetime "
                    "(%s) while time zone support is active."
                    % (self.model.__name__, self.model_field_name, value),
                    RuntimeWarning,
                )
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_aware(value, default_timezone)

            self.validate(value)
            return value

        try:
            parsed = parse_datetime(value)
            if parsed is not None:
                if settings.USE_TZ and timezone.is_naive(parsed):
                    if django.VERSION[:2] >= (4, 1):
                        default_timezone = timezone.get_default_timezone()
                    else:
                        default_timezone = timezone.utc
                    parsed = timezone.make_aware(parsed, default_timezone)
                self.validate(parsed)
                return parsed
        except ValueError as e:
            raise ValueError(f'Bad value: {value}') from e

        try:
            parsed = parse_date(value)
            if parsed is not None:
                value = datetime.datetime(parsed.year, parsed.month, parsed.day)
                self.validate(value)
                return value

        except ValueError as e:
            raise ValueError(f'Bad value: {value}') from e

        raise ValueError(f'Bad value: {value}')

    def to_db_value(self, value, instance):
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = timezone.now()
            setattr(instance, self.model_field_name, value)

        value = self.to_python_value(value)
        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            warnings.warn(
                "DateTimeField %s received a naive datetime (%s)"
                " while time zone support is active." % (self.model_field_name, value),
                RuntimeWarning,
            )
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_timezone)

        self.validate(value)
        return value


class TimeField(Field, datetime.time):
    skip_to_python_if_native = True
    SQL_TYPE = "TIME"

    class _db_oracle:
        SQL_TYPE = "TIMESTAMP"

    class _db_mysql:
        SQL_TYPE = "TIME(6)"

    def __init__(self, auto_now, auto_now_add, **kwargs):
        # Do not check combination of auto_now, auto_now_add, and default
        # since it has been done by Django
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_python_value(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.time):
            self.validate(value)
            return value
        if isinstance(value, datetime.datetime):
            # Not usually a good idea to pass in a datetime here (it loses
            # information), but this can be a side-effect of interacting with a
            # database backend (e.g. Oracle), so we'll be accommodating.
            value = value.time()
            self.validate(value)
            return value.time()

        try:
            parsed = parse_time(value)
            if parsed is not None:
                self.validate(parsed)
                return parsed
        except ValueError:
            raise ValueError(f'Bad value: {value}') from e

        raise ValueError(f'Bad value: {value}')

    def to_db_value(self, value, instance):

        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = datetime.datetime.now().time()
            setattr(instance, self.model_field_name, value)

        self.validate(value)

        from .models import DB_BACKEND
        if DB_BACKEND == 'postgresql':
            return value
        elif DB_BACKEND == 'sqlite3':
            return value.isoformat()

        raise NotImplementedError('Given database backend is not supported')


class DurationField(Field, datetime.timedelta):
    class _db_postgres:
        SQL_TYPE = 'INTERVAL'

    class _db_sqlite:
        SQL_TYPE = 'BIGINT'

    def to_python_value(self, value):
        if value is None or isinstance(value, datetime.timedelta):
            return value
        elif isinstance(value, int):
            return datetime.timedelta(microseconds=value)

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

        from .models import DB_BACKEND
        if DB_BACKEND == 'postgresql':
            return value
        elif DB_BACKEND == 'sqlite3':
            return duration_microseconds(value)

        raise NotImplementedError('Given database backend is not supported')


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
