#!/usr/bin/env python3
from typing import List

from lib.domain.file.interactor.file_list_interactor_helper import FileListInteractorHelper
from lib.domain.file.model.file import File
from lib.domain.file.repository.abstract_file_repository import AbstractFileRepository
from lib.usecase.file.list.abstract_file_list_usecase import AbstractFileListUseCase
from lib.usecase.file.list.file_list_input import FileListInput
from lib.usecase.file.list.file_list_output import FileListOutput


class FileListInteractor(AbstractFileListUseCase):
    __repository: AbstractFileRepository

    def __init__(self, repository: AbstractFileRepository):
        self.__repository = repository

    def handle(self, input_data: FileListInput) -> FileListOutput:
        FileListInteractorHelper.validate_input(input_data)
        params = FileListInteractorHelper.convert(input_data)
        FileListInteractorHelper.validate_param(params)
        files: List[File] = self.__repository.get_files_list(params)

        return FileListOutput(
            files=files
        )
