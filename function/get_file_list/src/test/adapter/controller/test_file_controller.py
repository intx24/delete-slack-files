import json
from http import HTTPStatus
from typing import Optional, Union, Dict
from unittest import TestCase

from lib.adapter.controller.file_controller import FileController
from lib.adapter.presenter.file_list_presenter_helper import FileListPresenterHelper
from lib.config.environment_variables import AbstractEnvironmentVariables
from lib.domain.file.model.file import File
from lib.usecase.file.list.abstract_file_list_presenter import AbstractFileListPresenter
from lib.usecase.file.list.abstract_file_list_usecase import AbstractFileListUseCase
from lib.usecase.file.list.file_list_input import FileListInput
from lib.usecase.file.list.file_list_output import FileListOutput


class MockFileListUseCase(AbstractFileListUseCase):
    def validate_input(self, input_data: FileListInput) -> None:
        pass

    def handle(self, input_data: FileListInput) -> FileListOutput:
        return FileListOutput(
            files=[File(
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
            ])


class MockEnvironmentVariables(AbstractEnvironmentVariables):
    token: str

    def __init__(self):
        self.token = 'token'


class MockFileListPresenter(AbstractFileListPresenter):
    def complete(self, output: FileListOutput, ex: Optional[Exception]) -> Dict[str, Union[int, Dict[str, str], str]]:
        return {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'files': [],
                'errors': []
            }, default=FileListPresenterHelper.default_method)
        }


class TestFileController(TestCase):
    controller: FileController

    def setUp(self) -> None:
        self.controller = FileController(MockFileListUseCase(), MockFileListPresenter(), MockEnvironmentVariables())

    def test_list(self):
        event = {
            'date_from': '2020-01-01',
            'date_to': '2020-11-11',
            'channel': 'channel',
            'user': 'user'
        }
        actual = self.controller.list(event)

        files = [File(
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

        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'files': [],
                'errors': []
            }, default=FileListPresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)
