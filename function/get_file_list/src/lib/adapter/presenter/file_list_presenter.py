#!/usr/bin/env python3
import json
import traceback
from http import HTTPStatus
from typing import Union, Optional, Dict

from lib.adapter.presenter.file_list_presenter_helper import FileListPresenterHelper
from lib.exception.environment_variables_exception import EnvironmentVariablesException
from lib.exception.external_api_call_exception import ExternalApiCallException
from lib.exception.validation_exception import ValidationException
from lib.usecase.file.list.abstract_file_list_presenter import AbstractFileListPresenter
from lib.usecase.file.list.file_list_output import FileListOutput


class FileListPresenter(AbstractFileListPresenter):
    def complete(self, output: FileListOutput, e: Optional[Exception]) -> \
            Dict[str, Union[int, Dict[str, str], str]]:
        if e is None:
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

        e_message = ''.join(traceback.TracebackException.from_exception(e).format())

        if isinstance(e, EnvironmentVariablesException):
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': [],
                    'errors': [
                        f'env var exception: {e_message}'
                    ]
                }, default=FileListPresenterHelper.default_method)
            }
        elif isinstance(e, ValidationException):
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': [],
                    'errors': [
                        f'validation exception: {e_message}'
                    ]
                }, default=FileListPresenterHelper.default_method)
            }
        elif isinstance(e, ExternalApiCallException):
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'files': [],
                    'errors': [
                        f'external api error: {e_message}'
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
                        f'exception: {e_message}'
                    ]
                }, default=FileListPresenterHelper.default_method)
            }
