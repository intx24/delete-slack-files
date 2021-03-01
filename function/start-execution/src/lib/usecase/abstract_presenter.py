#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod
from typing import Union, Optional, Dict


class AbstractPresenter(metaclass=ABCMeta):
    @abstractmethod
    def complete(self, ex: Optional[Exception]) -> Dict[str, Union[int, Dict[str, str], str]]:
        pass
