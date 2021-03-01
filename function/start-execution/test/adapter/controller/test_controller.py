import base64
import json
from http import HTTPStatus
from typing import Optional, Union, Dict
from unittest import TestCase, mock
from urllib.parse import urlencode

from lib.adapter.controller.controller import Controller
from lib.adapter.presenter.presenter_helper import PresenterHelper
from lib.config.environment_variables import AbstractEnvironmentVariables
from lib.usecase.abstract_presenter import AbstractPresenter


class MockEnvironmentVariables(AbstractEnvironmentVariables):
    slack_signing_secret: str
    stage: str

    def __init__(self):
        self.slack_signing_secret = 'secret'
        self.stage = 'test'


class MockPresenter(AbstractPresenter):
    def complete(self, e: Optional[Exception]) -> Dict[str, Union[int, Dict[str, str], str]]:
        if e is not None:
            raise e

        return {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps('start execution.', default=PresenterHelper.default_method)
        }


class TestController(TestCase):
    __controller: Controller

    def setUp(self) -> None:
        self.__controller = Controller(MockPresenter(), MockEnvironmentVariables())

    @mock.patch('time.time')
    def test_execute__ok(self, mock_time):
        mock_time.return_value = 1577804400

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
                'x-slack-signature': 'v0=ae57e7b278aa947c4aae097caf4e221c04b9323a738db24a57d868f86766f5c5'
            },
            'body': encoded
        }
        actual = self.__controller.execute(event)

        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps('start execution.', default=PresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)
