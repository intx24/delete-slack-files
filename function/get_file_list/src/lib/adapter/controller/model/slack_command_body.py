#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(frozen=True)
class SlackCommandBody:
    token: str
    user_id: str
    channel_id: str
    command: str
    text: str
