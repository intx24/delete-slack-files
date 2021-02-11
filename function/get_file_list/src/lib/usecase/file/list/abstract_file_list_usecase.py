#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod

from lib.usecase.file.list.file_list_input import FileListInput
from lib.usecase.file.list.file_list_output import FileListOutput


class AbstractFileListUseCase(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, input_data: FileListInput) -> FileListOutput:
        pass
