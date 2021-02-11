from enum import Enum


class ResultCode(Enum):
    SUCCESS = 1
    VALIDATION_ERROR = 2
    DATA_ACCESS_ERROR = 3
    INTERNAL_ERROR = 4
