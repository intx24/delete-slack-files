import unittest
from typing import List
from unittest import TestCase

from lib.domain.file.interactor.file_list_interactor import FileListInteractor
from lib.domain.file.model.file import File
from lib.domain.file.model.get_files_list_params import GetFilesListParams
from lib.domain.file.repository.abstract_file_repository import AbstractFileRepository
from lib.usecase.file.list.file_list_input import FileListInput


class MockFileRepository(AbstractFileRepository):
    def get_files_list(self, params: GetFilesListParams) -> List[File]:
        return [File(
            id='id1',
            created=1612611194,
            timestamp=1612611194,
            name='IMG_1.jpg',
            title='IMG_1.jpg',
            mimetype='image/jpeg',
            filetype='jpg',
            user='user1',
            size=1,
            is_public=False,
            username='',
            url_private='url_private1',
            url_private_download='url_private_download1')
        ]


class TestFileListInteractor(TestCase):
    interactor: FileListInteractor

    def setUp(self) -> None:
        self.interactor = FileListInteractor(MockFileRepository())

    def test_handle(self):
        input_data: FileListInput = FileListInput(
            token='token',
            date_from='2020/01/01',
            date_to='2020/11/11',
            channel='channel',
            user='user'
        )

        actual = self.interactor.handle(input_data)
        expected = [File(
            id='id1',
            created=1612611194,
            timestamp=1612611194,
            name='IMG_1.jpg',
            title='IMG_1.jpg',
            mimetype='image/jpeg',
            filetype='jpg',
            user='user1',
            size=1,
            is_public=False,
            username='',
            url_private='url_private1',
            url_private_download='url_private_download1')
        ]
        self.assertListEqual(expected, actual.files)


if __name__ == '__main__':
    unittest.main()
