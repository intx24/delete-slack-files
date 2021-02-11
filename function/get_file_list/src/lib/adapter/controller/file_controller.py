#!/usr/bin/env python3
from typing import Union, Dict

from lib.adapter.controller.file_controller_helper import FileControllerHelper
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
            FileControllerHelper.validate_list_event(event)

            input_data: FileListInput = FileListInput(
                token=self.__env_vars.token,
                date_from=event['date_from'],
                date_to=event['date_to'],
                channel=event['channel'] if 'channel' in event else None,
                user=event['user'] if 'user' in event else None,
            )

            output: FileListOutput = self.__usecase.handle(input_data)
            return self.__presenter.complete(output, None)
        except Exception as ex:
            return self.__presenter.complete(FileListOutput([]), ex)
