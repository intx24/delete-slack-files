#!/usr/bin/env python3

import dataclasses
from typing import List

from lib.domain.file.model.file import File


@dataclasses.dataclass(frozen=True)
class FileListOutput:
    files: List[File]
