import cgi
import csv
import io
import re
from functools import (
    partial,
)


def join_parts(parts, delimiter=';'):
    return delimiter.join(parts)


join_lines = partial(join_parts, delimiter='\n')


def try_decode_csv(value) -> str:
    """Проверка возможности декодирования csv."""

    delimiter_ = ';'

    if issubclass(type(value), bytes):
        value = value.decode('utf-8')

    reader = csv.reader(io.StringIO(value), delimiter=delimiter_)

    result = join_lines(
        join_parts(parts) for parts in reader
    )
    return result


def try_decode_multipart(value):
    boundary = re.compile(
        '(--){1}([a-z1-90]{32})(\\r\\n).*'
    ).match(
        value.decode('utf-8')
    )[2]

    result = cgi.parse_multipart(
        io.BytesIO(value),
        {
            'boundary': boundary.encode('ASCII')
        }
    )
    return result
