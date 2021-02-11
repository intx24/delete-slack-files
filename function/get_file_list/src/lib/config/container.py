#!/usr/bin/env python3
from dataclasses import dataclass

from lib.adapter.controller.file_controller import FileController
from lib.adapter.presenter.file_list_presenter import FileListPresenter
from lib.config.environment_variables import EnvironmentVariables
from lib.config.singleton import Singleton
from lib.domain.file.interactor.file_list_interactor import FileListInteractor
from lib.domain.file.repository.abstract_file_repository import AbstractFileRepository
from lib.driver.api.slack_driver import SlackDriver
from lib.usecase.file.list.abstract_file_list_presenter import AbstractFileListPresenter
from lib.usecase.file.list.abstract_file_list_usecase import AbstractFileListUseCase


@dataclass
class Container(Singleton):
    file_list_repository: AbstractFileRepository = None
    file_list_usecase: AbstractFileListUseCase = None
    file_controller: FileController = None
    file_list_presenter: AbstractFileListPresenter = None
    environment_variables: EnvironmentVariables = None

    def slack_inject(self):
        repository_impl = SlackDriver()
        usecase_impl = FileListInteractor(repository_impl)
        env_vars_impl = EnvironmentVariables()
        presenter_impl = FileListPresenter()
        controller = FileController(
            usecase=usecase_impl,
            presenter=presenter_impl,
            env_vars=env_vars_impl)

        self.file_list_repository = SlackDriver()
        self.file_list_usecase = usecase_impl
        self.file_list_presenter = presenter_impl
        self.environment_variables = env_vars_impl
        self.file_controller = controller
