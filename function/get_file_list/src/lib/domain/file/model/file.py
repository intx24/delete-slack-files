#!/usr/bin/env python3

import dataclasses


@dataclasses.dataclass(frozen=True)
class File:
    id: str
    created: int
    timestamp: int
    name: str
    title: str
    mimetype: str
    filetype: str
    user: str
    size: int
    is_public: bool
    username: str
    url_private: str
    url_private_download: str
