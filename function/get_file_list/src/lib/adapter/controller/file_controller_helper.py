#!/usr/bin/env python3
import base64
import re
from typing import Dict, List
from urllib.parse import parse_qs

from lib.adapter.controller.model.parsed_text import ParsedText
from lib.adapter.controller.model.slack_command_body import SlackCommandBody
from lib.exception.validation_exception import ValidationException


class FileControllerHelper:
    @staticmethod
    def get_command_body(event: Dict) -> SlackCommandBody:
        body = event['body']
        decoded = base64.b64decode(body).decode()
        decoded_dict = parse_qs(decoded)

        return SlackCommandBody(
            token=decoded_dict['token'][0],
            user_id=decoded_dict['user_id'][0],
            channel_id=decoded_dict['channel_id'][0],
            command=decoded_dict['command'][0],
            text=decoded_dict['text'][0]
        )

    @staticmethod
    def parse_text(text: str) -> ParsedText:
        splitted: List[str] = text.split()
        from_part = next(filter(lambda s: s.startsWith("from="), splitted), None)
        to_part = next(filter(lambda s: s.startsWith("to="), splitted), None)

        return ParsedText(
            date_from=from_part.lstrip("from=").strip(),
            date_to=to_part.lstrip("to=").strip(),
            all_channels="--all-channels" in splitted or "-ac" in splitted,
            all_users="--all-users" in splitted or "-au" in splitted
        )

    @staticmethod
    def validate_body(body: SlackCommandBody):
        try:
            valid = True
            valid = valid and bool(body.token)
            valid = valid and bool(body.user_id)
            valid = valid and bool(body.channel_id)
            valid = valid and bool(body.command)
            valid = valid and bool(body.text)

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
