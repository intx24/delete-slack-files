#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedText:
    date_to: str
    date_from: str
    all_channels: bool
    all_users: bool
