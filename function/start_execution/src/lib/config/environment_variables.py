#!/usr/bin/env python3
import os
from abc import ABCMeta

from lib.exception.environment_variables_exception import EnvironmentVariablesException


class AbstractEnvironmentVariables(metaclass=ABCMeta):
    stage: str
    slack_signing_secret: str


class EnvironmentVariables(AbstractEnvironmentVariables):
    stage: str
    slack_signing_secret: str

    def __init__(self):
        stage = os.getenv('STAGE', None)
        slack_signing_secret = os.getenv('SLACK_SIGNING_SECRET', None)

        if not stage:
            raise EnvironmentVariablesException('stage does not exists')

        if not slack_signing_secret:
            raise EnvironmentVariablesException('signing_secret does not exists')

        self.stage = stage
        self.slack_signing_secret = slack_signing_secret
