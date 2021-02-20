#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(frozen=True)
class SlashCommandHeaders:
    slack_request_timestamp: int
    slack_signature: str
