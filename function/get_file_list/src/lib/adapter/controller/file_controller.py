#!/usr/bin/env python3
from typing import Union, Dict

from lib.adapter.controller.file_controller_helper import FileControllerHelper
from lib.adapter.controller.model.parsed_text import ParsedText
from lib.adapter.controller.model.slash_command_body import SlashCommandBody
from lib.adapter.controller.model.slash_command_headers import SlashCommandHeaders
from lib.config.environment_variables import AbstractEnvironmentVariables
from lib.exception.invalid_signature_expection import InvalidSignatureException
from lib.exception.invalid_timestamp_exception import InvalidTimestampException
from lib.usecase.file.list.abstract_file_list_presenter import AbstractFileListPresenter
from lib.usecase.file.list.abstract_file_list_usecase import AbstractFileListUseCase
from lib.usecase.file.list.file_list_input import FileListInput
from lib.usecase.file.list.file_list_output import FileListOutput


class FileController:
    def __init__(self, usecase: AbstractFileListUseCase, presenter: AbstractFileListPresenter,
                 env_vars: AbstractEnvironmentVariables):
        self.__usecase = usecase
        self.__presenter = presenter
        self.__env_vars = env_vars

    def list(self, event: Dict) -> Dict[str, Union[int, Dict[str, str], str]]:
        try:
            is_local = self.__env_vars.stage == 'local'

            valid_timestamp = True
            valid_signature = True
            if not is_local:
                headers: SlashCommandHeaders = FileControllerHelper.get_command_header(event)

                raw_body = FileControllerHelper.get_raw_body(event)
                valid_signature = FileControllerHelper.valid_signature(
                    headers,
                    raw_body,
                    self.__env_vars.slack_signing_secret)
                valid_timestamp = FileControllerHelper.valid_timestamp(headers.slack_request_timestamp)
            if not valid_timestamp:
                raise InvalidTimestampException(event['headers'])
            if not valid_signature:
                raise InvalidSignatureException(event['headers'])

            body: SlashCommandBody = FileControllerHelper.get_command_body(event)
            FileControllerHelper.validate_body(body)
            parsed_text: ParsedText = FileControllerHelper.parse_text(body.text)

            input_data: FileListInput = FileListInput(
                token=self.__env_vars.token,
                date_from=parsed_text.date_from,
                date_to=parsed_text.date_to,
                channel=body.channel_id if parsed_text.all_channels else None,
                user=body.user_id if parsed_text.all_users else None,
            )

            output: FileListOutput = self.__usecase.handle(input_data)
            return self.__presenter.complete(output, None)
        except Exception as ex:
            return self.__presenter.complete(FileListOutput([]), ex)
