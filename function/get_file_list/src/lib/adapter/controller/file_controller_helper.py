#!/usr/bin/env python3
import base64
import hashlib
import hmac
import re
import time
from typing import Dict, List
from urllib.parse import parse_qs

from lib.adapter.controller.model.parsed_text import ParsedText
from lib.adapter.controller.model.slash_command_body import SlashCommandBody
from lib.adapter.controller.model.slash_command_headers import SlashCommandHeaders
from lib.exception.validation_exception import ValidationException


class FileControllerHelper:
    @staticmethod
    def get_command_header(event: Dict) -> SlashCommandHeaders:
        headers = event['headers']

        return SlashCommandHeaders(
            slack_request_timestamp=int(headers['x-slack-request-timestamp']),
            slack_signature=headers['x-slack-signature'],
        )

    @staticmethod
    def get_raw_body(event: Dict) -> str:
        body = event['body']
        return base64.b64decode(body).decode()

    @staticmethod
    def get_command_body(event: Dict) -> SlashCommandBody:
        raw_body = FileControllerHelper.get_raw_body(event)
        decoded_dict = parse_qs(raw_body)

        return SlashCommandBody(
            token=decoded_dict['token'][0],
            user_id=decoded_dict['user_id'][0],
            channel_id=decoded_dict['channel_id'][0],
            command=decoded_dict['command'][0],
            text=decoded_dict['text'][0]
        )

    @staticmethod
    def parse_text(text: str) -> ParsedText:
        splitted: List[str] = text.split()
        from_part = next(filter(lambda s: s.startswith("from="), splitted), None)
        to_part = next(filter(lambda s: s.startswith("to="), splitted), None)

        return ParsedText(
            date_from=from_part.lstrip("from=").strip(),
            date_to=to_part.lstrip("to=").strip(),
            all_channels="--all-channels" in splitted or "-ac" in splitted,
            all_users="--all-users" in splitted or "-au" in splitted
        )

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

    @staticmethod
    def validate_body(body: SlashCommandBody):
        try:
            valid = True
            validate_exist_targets: List[str] = [
                body.token,
                body.user_id,
                body.channel_id,
                body.command,
                body.text
            ]
            for t in validate_exist_targets:
                valid = valid and bool(t)

            text_splitted: List[str] = body.text.split()
            date_pattern: str = r'[12]\d{3}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])'

            to_part = next(filter(lambda s: s.startswith("to="), text_splitted), None)
            valid = valid and to_part is not None
            valid = valid and re.match(date_pattern, to_part.lstrip("to="))

            from_part = next(filter(lambda s: s.startswith("from="), text_splitted), None)
            valid = valid and from_part is not None
            valid = valid and re.match(date_pattern, from_part.lstrip("from="))

        except Exception as e:
            raise ValidationException(f'invalid body {e}', e)
        else:
            if not valid:
                raise ValidationException('invalid body')
