#!/usr/bin/env python3


class FileListPresenterHelper:
    @staticmethod
    def default_method(item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError
