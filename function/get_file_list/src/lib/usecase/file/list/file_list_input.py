#!/usr/bin/env python3

import dataclasses
from datetime import datetime

from typing import Optional


@dataclasses.dataclass(frozen=True)
class FileListInput:
    token: str
    date_from: str
    date_to: str
    channel: Optional[str] = None
    user: Optional[str] = None

    def ts_from(self):
        from_date: datetime = datetime.strptime(self.date_from, '%Y/%m/%d')
        return from_date.timestamp()

    def ts_to(self):
        to_date: datetime = datetime.strptime(self.date_to, '%Y/%m/%d')
        return to_date.timestamp()
