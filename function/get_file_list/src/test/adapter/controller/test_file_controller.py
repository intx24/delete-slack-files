import base64
import json
from http import HTTPStatus
from typing import Optional, Union, Dict
from unittest import TestCase
from urllib.parse import urlencode

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
    slack_signing_secret: str

    def __init__(self):
        self.slack_signing_secret = 'secret'


class MockFileListPresenter(AbstractFileListPresenter):
    def complete(self, output: FileListOutput, ex: Optional[Exception]) -> Dict[str, Union[int, Dict[str, str], str]]:
        if ex is not None:
            raise ex

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

    def test_list__ok(self):
        body: Dict = {
            'token': 'token_1',
            'user_id': 'user_id1',
            'channel_id': 'channel_id1',
            'command': 'command_1',
            'text': 'to=2020/01/01 from=2020/11/11',
        }
        encoded_dict = urlencode(body)
        encoded = base64.b64encode(encoded_dict.encode('utf-8'))
        event: Dict = {
            'headers': {
                'x-slack-request-timestamp': '1577804400',
                'x-slack-signature': 'v0=ce8c8e193a9b6f69d6c3ed897d781d43cff0553eca5e067013dbc9b652a85edc'
            },
            'body': encoded
        }
        actual = self.controller.list(event)

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
