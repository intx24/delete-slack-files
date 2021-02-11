#!/usr/bin/env python3
from datetime import datetime
from typing import Dict

from lib.exception.validation_exception import ValidationException


class FileControllerHelper:
    @staticmethod
    def validate_list_event(event: Dict):
        try:
            is_not_empty_str = all(
                map(lambda s: bool(s), [event['date_to'], event['date_from']]))
            is_not_empty_str_or_none = all(
                map(lambda s: s not in event or str.strip(event[s]) != '', ['user', 'channel']))
            datetime.strptime(event['date_to'], '%Y-%m-%d')
            datetime.strptime(event['date_from'], '%Y-%m-%d')
            can_convert = True
        except Exception as e:
            raise ValidationException(f'eventの引数が不正です: {e}', e)
        else:
            valid = is_not_empty_str and is_not_empty_str_or_none and can_convert
            if not valid:
                raise ValidationException('eventの引数が不正です')
