import json
from http import HTTPStatus
from unittest import TestCase

from lib.adapter.presenter.presenter import Presenter
from lib.adapter.presenter.presenter_helper import PresenterHelper
from lib.exception.environment_variables_exception import EnvironmentVariablesException
from lib.exception.invalid_signature_exception import InvalidSignatureException
from lib.exception.invalid_timestamp_exception import InvalidTimestampException
from lib.usecase.abstract_presenter import AbstractPresenter


class TestPresenter(TestCase):
    __presenter: AbstractPresenter

    def setUp(self) -> None:
        self.__presenter = Presenter()

    def test_complete__ok(self):
        actual = self.__presenter.complete(None)
        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps('start execution.', default=PresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)

    def test_complete__raise_environment_variables_exception(self):
        actual = self.__presenter.complete(EnvironmentVariablesException('e_test'))
        expected = {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'headers': {
                'Content-Type': 'application/json'
            },
        }

        self.assertEqual(expected['statusCode'], actual['statusCode'])
        self.assertEqual(expected['headers'], actual['headers'])
        self.assertTrue('e_test' in actual['body'])
        self.assertTrue('env var exception' in actual['body'])


    def test_complete__raise_invalid_signature_exception(self):
        actual = self.__presenter.complete(InvalidSignatureException('signature_test'))
        expected = {
            'statusCode': HTTPStatus.FORBIDDEN,
            'headers': {
                'Content-Type': 'application/json'
            },
        }

        self.assertEqual(expected['statusCode'], actual['statusCode'])
        self.assertEqual(expected['headers'], actual['headers'])
        self.assertTrue('signature_test' in actual['body'])
        self.assertTrue('invalid signature' in actual['body'])

    def test_complete__raise_invalid_timestamp_exception(self):
        actual = self.__presenter.complete(InvalidTimestampException('signature_test'))
        expected = {
            'statusCode': HTTPStatus.FORBIDDEN,
            'headers': {
                'Content-Type': 'application/json'
            },
        }

        self.assertEqual(expected['statusCode'], actual['statusCode'])
        self.assertEqual(expected['headers'], actual['headers'])
        self.assertTrue('signature_test' in actual['body'])
        self.assertTrue('invalid timestamp' in actual['body'])

    def test_complete__raise_exception(self):
        actual = self.__presenter.complete(Exception('test'))
        expected = {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'headers': {
                'Content-Type': 'application/json'
            },
        }

        self.assertEqual(expected['statusCode'], actual['statusCode'])
        self.assertEqual(expected['headers'], actual['headers'])
        self.assertTrue('test' in actual['body'])
