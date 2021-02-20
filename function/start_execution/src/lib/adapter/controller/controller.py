#!/usr/bin/env python3
from typing import Union, Dict

from lib.adapter.controller.controller_helper import ControllerHelper
from lib.adapter.controller.model.slash_command import SlashCommandHeaders
from lib.config.environment_variables import AbstractEnvironmentVariables
from lib.exception.invalid_signature_exception import InvalidSignatureException
from lib.exception.invalid_timestamp_exception import InvalidTimestampException
from lib.usecase.abstract_presenter import AbstractPresenter


class Controller:
    def __init__(self, presenter: AbstractPresenter, env_vars: AbstractEnvironmentVariables) -> object:
        self.__presenter = presenter
        self.__env_vars = env_vars

    def execute(self, event: Dict) -> Dict[str, Union[int, Dict[str, str], str]]:
        try:
            is_local = self.__env_vars.stage == 'local'

            valid_timestamp = True
            valid_signature = True
            if not is_local:
                headers: SlashCommandHeaders = ControllerHelper.get_command_header(event)

                raw_body = ControllerHelper.get_raw_body(event)
                valid_signature = ControllerHelper.valid_signature(
                    headers,
                    raw_body,
                    self.__env_vars.slack_signing_secret)
                valid_timestamp = ControllerHelper.valid_timestamp(headers.slack_request_timestamp)
            if not valid_timestamp:
                raise InvalidTimestampException(event['headers'])
            if not valid_signature:
                raise InvalidSignatureException(event['headers'])

            # TODO: execute step function with request param

            return self.__presenter.complete(None)
        except Exception as e:
            return self.__presenter.complete(e)
