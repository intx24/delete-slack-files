#!/usr/bin/env python3
import json
import traceback
from http import HTTPStatus
from typing import Optional, Dict, Union

from lib.adapter.presenter.presenter_helper import PresenterHelper
from lib.exception.environment_variables_exception import EnvironmentVariablesException
from lib.exception.invalid_signature_exception import InvalidSignatureException
from lib.exception.invalid_timestamp_exception import InvalidTimestampException
from lib.usecase.abstract_presenter import AbstractPresenter


class Presenter(AbstractPresenter):
    def complete(self, e: Optional[Exception]) -> \
            Dict[str, Union[int, Dict[str, str], str]]:

        headers = {
            'Content-Type': 'application/json'
        }
        if e is None:
            return {
                'statusCode': HTTPStatus.OK,
                'headers': headers,
                'body': json.dumps('start execution.')
            }

        e_message = ''.join(traceback.TracebackException.from_exception(e).format())

        if isinstance(e, EnvironmentVariablesException):
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': headers,
                'body': json.dumps(f'env var exception: {e_message}',
                                   default=PresenterHelper.default_method)
            }
        elif isinstance(e, InvalidSignatureException):
            return {
                'statusCode': HTTPStatus.FORBIDDEN,
                'headers': headers,
                'body': json.dumps(f'invalid signature: {e_message}',
                                   default=PresenterHelper.default_method)
            }
        elif isinstance(e, InvalidTimestampException):
            return {
                'statusCode': HTTPStatus.FORBIDDEN,
                'headers': headers,
                'body': json.dumps(f'invalid timestamp: {e_message}',
                                   default=PresenterHelper.default_method)
            }
        else:
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'headers': headers,
                'body': json.dumps(f'error: {e_message}',
                                   default=PresenterHelper.default_method)
            }
