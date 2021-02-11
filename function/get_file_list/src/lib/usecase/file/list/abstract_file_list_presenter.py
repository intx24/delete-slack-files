#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod
from typing import Union, Optional, Dict

from lib.usecase.file.list.file_list_output import FileListOutput


class AbstractFileListPresenter(metaclass=ABCMeta):
    @abstractmethod
    def complete(self, output: FileListOutput, ex: Optional[Exception]) -> Dict[str, Union[int, Dict[str, str], str]]:
        pass
