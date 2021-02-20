#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(frozen=True)
class SlashCommandHeaders:
    slack_request_timestamp: int
    slack_signature: str


@dataclass(frozen=True)
class SlashCommandBody:
    token: str
    user_id: str
    channel_id: str
    command: str
    text: str


@dataclass(frozen=True)
class SlashCommand:
    headers: SlashCommandHeaders
    body: SlashCommandBody
