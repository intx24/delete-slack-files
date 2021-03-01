#!/usr/bin/env python3
import base64
import hashlib
import hmac
import re
import time
from typing import Dict, List
from urllib.parse import parse_qs

from lib.adapter.controller.model.slash_command import SlashCommandHeaders, SlashCommandBody


class ControllerHelper:
    @staticmethod
    def get_command_header(event: Dict) -> SlashCommandHeaders:
        headers = event['headers']

        return SlashCommandHeaders(
            slack_request_timestamp=int(headers['x-slack-request-timestamp']),
            slack_signature=headers['x-slack-signature'],
        )

    @staticmethod
    def get_command_body(event: Dict) -> SlashCommandBody:
        raw_body = ControllerHelper.get_raw_body(event)
        decoded_dict = parse_qs(raw_body)

        return SlashCommandBody(
            token=decoded_dict['token'][0],
            user_id=decoded_dict['user_id'][0],
            channel_id=decoded_dict['channel_id'][0],
            command=decoded_dict['command'][0],
            text=decoded_dict['text'][0]
        )

    @staticmethod
    def get_raw_body(event: Dict) -> str:
        """

        :rtype: object
        """
        body = event['body']
        return base64.b64decode(body).decode()

    @staticmethod
    def valid_signature(headers: SlashCommandHeaders, raw_body: str, secret: str) -> bool:
        base_str = f'v0:{headers.slack_request_timestamp}:{raw_body}'

        secret_hmac = hmac.new(secret.encode('utf-8'), base_str.encode('utf-8'), hashlib.sha256).hexdigest()
        expected = f'v0={secret_hmac}'
        actual = headers.slack_signature
        return hmac.compare_digest(expected, actual)

    @staticmethod
    def valid_timestamp(timestamp: int) -> bool:
        return abs(time.time() - timestamp) <= 60 * 5

