#!/usr/bin/env python3

from lib.domain.file.model.get_files_list_params import GetFilesListParams
from lib.exception.validation_exception import ValidationException
from lib.usecase.file.list.file_list_input import FileListInput


class FileListInteractorHelper:
    @staticmethod
    def convert(input_data: FileListInput) -> GetFilesListParams:
        params: GetFilesListParams = GetFilesListParams(
            token=input_data.token,
            channel=input_data.channel,
            ts_from=input_data.ts_from(),
            ts_to=input_data.ts_to(),
            user=input_data.user
        )
        return params

    @staticmethod
    def validate_input(input_data: FileListInput):
        try:
            is_not_empty_str = all(map(lambda s: bool(s), [input_data.token, input_data.date_to, input_data.date_from]))
            is_not_empty_str_or_none = all(
                map(lambda s: s is None or str.strip(s) != '', [input_data.user, input_data.channel]))

            input_data.ts_to()
            input_data.ts_from()
            can_convert = True
        except Exception as e:
            raise ValidationException(f'inputの値が不正です: {e}', e)
        else:
            valid = is_not_empty_str and is_not_empty_str_or_none and can_convert

            if not valid:
                raise ValidationException('inputの値が不正です')

    @staticmethod
    def validate_param(params: GetFilesListParams):
        try:
            is_not_empty_str_or_none = all(
                map(lambda s: s is None or str.strip(s) != '', [params.user, params.channel]))
        except Exception as e:
            raise ValidationException(f'paramsの値が不正です: {e}', e)
        else:
            valid = is_not_empty_str_or_none

            if not valid:
                raise ValidationException('paramsの値が不正です')
