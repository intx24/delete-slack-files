#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetFilesListParams:
    token: str
    ts_from: int
    ts_to: int
    channel: Optional[str] = None
    user: Optional[str] = None
