#!/usr/bin/env python3
import json
from http import HTTPStatus
from typing import Union, Optional, Dict

from lib.adapter.presenter.file_list_presenter_helper import FileListPresenterHelper
from lib.exception.environment_variables_exception import EnvironmentVariablesException
from lib.exception.validation_exception import ValidationException
from lib.usecase.file.list.abstract_file_list_presenter import AbstractFileListPresenter
from lib.usecase.file.list.file_list_output import FileListOutput


class FileListPresenter(AbstractFileListPresenter):
    def complete(self, output: FileListOutput, ex: Optional[Exception]) -> \
            Dict[str, Union[int, Dict[str, str], str]]:
        if ex is None:
            return {
                'statusCode': HTTPStatus.OK,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': output.files,
                    'errors': []
                }, default=FileListPresenterHelper.default_method)
            }
        elif isinstance(ex, EnvironmentVariablesException):
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': [],
                    'errors': [
                        f'env var exception: {ex}'
                    ]
                }, default=FileListPresenterHelper.default_method)
            }
        elif isinstance(ex, ValidationException):
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': [],
                    'errors': [
                        f'validation exception: {ex}'
                    ]
                }, default=FileListPresenterHelper.default_method)
            }
        else:
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': [],
                    'errors': [
                        f'exception: {ex}'
                    ]
                }, default=FileListPresenterHelper.default_method)
            }
