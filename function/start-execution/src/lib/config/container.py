#!/usr/bin/env python3
from dataclasses import dataclass

from lib.adapter.controller.controller import Controller
from lib.adapter.presenter.presenter import Presenter
from lib.config.environment_variables import EnvironmentVariables
from lib.config.singleton import Singleton
from lib.usecase.abstract_presenter import AbstractPresenter


@dataclass
class Container(Singleton):
    controller: Controller = None
    presenter: AbstractPresenter = None
    environment_variables: EnvironmentVariables = None

    def slack_inject(self):
        env_vars_impl = EnvironmentVariables()
        presenter_impl = Presenter()
        controller = Controller(
            presenter=presenter_impl,
            env_vars=env_vars_impl)

        self.presenter = presenter_impl
        self.environment_variables = env_vars_impl
        self.controller = controller
