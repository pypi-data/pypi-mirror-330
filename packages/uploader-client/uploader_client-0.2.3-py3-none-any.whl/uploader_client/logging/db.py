# coding: utf-8


from dataclasses import (
    asdict,
)
from typing import (
    Optional,
)

from ..models import (
    Entry as DBEntry,
)
from .base import (
    AbstractLogger,
    Entry,
)


class Logger(AbstractLogger):

    def log(self, entry: Entry) -> Optional[DBEntry]:

        assert isinstance(entry, Entry)

        db_entry = DBEntry.objects.create(**asdict(entry))

        return db_entry
