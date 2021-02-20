#!/usr/bin/env python3
import os
from abc import ABCMeta

from lib.exception.environment_variables_exception import EnvironmentVariablesException


class AbstractEnvironmentVariables(metaclass=ABCMeta):
    slack_signing_secret: str


class EnvironmentVariables(AbstractEnvironmentVariables):
    slack_signing_secret: str

    def __init__(self):
        token = os.getenv('SLACK_SIGNING_SECRET')

        if not token:
            raise EnvironmentVariablesException('signing_secret does not exists')

        self.token = token
