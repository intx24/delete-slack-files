#!/usr/bin/env python3
import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class SlashCommandHeaders:
    slack_request_timestamp: datetime
    slack_signature: str
