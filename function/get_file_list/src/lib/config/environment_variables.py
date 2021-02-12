#!/usr/bin/env python3
import os
from abc import ABCMeta

from lib.exception.environment_variables_exception import EnvironmentVariablesException


class AbstractEnvironmentVariables(metaclass=ABCMeta):
    token: str


class EnvironmentVariables(AbstractEnvironmentVariables):
    token: str

    def __init__(self):
        token = os.getenv('SLACK_API_TOKEN')

        if not token:
            raise EnvironmentVariablesException('token does not exists')

        self.token = token
