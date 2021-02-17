#!/usr/bin/env python3
from typing import Union, Dict

from lib.adapter.controller.file_controller_helper import FileControllerHelper
from lib.adapter.controller.model.parsed_text import ParsedText
from lib.adapter.controller.model.slack_command_body import SlackCommandBody
from lib.config.environment_variables import AbstractEnvironmentVariables
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
            body: SlackCommandBody = FileControllerHelper.get_command_body(event)
            FileControllerHelper.validate_body(body)
            parsed_text: ParsedText = FileControllerHelper.parse_text(body.text)

            input_data: FileListInput = FileListInput(
                token=body.token,
                date_from=parsed_text.date_from,
                date_to=parsed_text.date_to,
                channel=body.channel_id if parsed_text.all_channels else None,
                user=body.user_id if parsed_text.all_users else None,
            )

            output: FileListOutput = self.__usecase.handle(input_data)
            return self.__presenter.complete(output, None)
        except Exception as ex:
            return self.__presenter.complete(FileListOutput([]), ex)
