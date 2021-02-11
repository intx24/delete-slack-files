import json
from http import HTTPStatus
from unittest import TestCase

from lib.adapter.presenter.file_list_presenter import FileListPresenter
from lib.adapter.presenter.file_list_presenter_helper import FileListPresenterHelper
from lib.domain.file.model.file import File
from lib.exception.environment_variables_exception import EnvironmentVariablesException
from lib.exception.validation_exception import ValidationException
from lib.usecase.file.list.abstract_file_list_presenter import AbstractFileListPresenter
from lib.usecase.file.list.file_list_output import FileListOutput


class TestFileListPresenter(TestCase):
    __presenter: AbstractFileListPresenter

    def setUp(self) -> None:
        self.__presenter = FileListPresenter()

    def test_complete__ok(self):
        output = FileListOutput(
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

        actual = self.__presenter.complete(output, None)
        expected = {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'files': output.files,
                'errors': []
            }, default=FileListPresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)

    def test_complete__raise_validation_exception(self):
        actual = self.__presenter.complete(FileListOutput([]), ValidationException('v_test'))
        expected = {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'files': [],
                'errors': [
                    'validation exception: v_test'
                ]
            }, default=FileListPresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)

    def test_complete__raise_environment_variables_exception(self):
        actual = self.__presenter.complete(FileListOutput([]), EnvironmentVariablesException('e_test'))
        expected = {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'files': [],
                'errors': [
                    'env var exception: e_test'
                ]
            }, default=FileListPresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)

    def test_complete__raise_exception(self):
        actual = self.__presenter.complete(FileListOutput([]), Exception('test'))
        expected = {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'files': [],
                'errors': [
                    'exception: test'
                ]
            }, default=FileListPresenterHelper.default_method)
        }

        self.assertEqual(expected, actual)
