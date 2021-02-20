#!/usr/bin/env python3
import os
from abc import ABCMeta

from lib.exception.environment_variables_exception import EnvironmentVariablesException


class AbstractEnvironmentVariables(metaclass=ABCMeta):
    token: str
    stage: str
    slack_signing_secret: str


class EnvironmentVariables(AbstractEnvironmentVariables):
    token: str = None
    stage: str
    slack_signing_secret: str

    def __init__(self):
        token = os.getenv('SLACK_API_TOKEN', None)
        stage = os.getenv('STAGE', None)
        slack_signing_secret = os.getenv('SLACK_SIGNING_SECRET', None)

        if not stage:
            raise EnvironmentVariablesException('stage does not exists')

        if not slack_signing_secret:
            raise EnvironmentVariablesException('signing_secret does not exists')

        self.token = token
        self.stage = stage
        self.slack_signing_secret = slack_signing_secret
