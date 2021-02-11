from abc import ABCMeta, abstractmethod
from typing import List

from lib.domain.file.model.file import File
from lib.domain.file.model.get_files_list_params import GetFilesListParams


class AbstractFileRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_files_list(self, params: GetFilesListParams) -> List[File]:
        pass
