#!/usr/bin/env python3

class Singleton(object):
    @classmethod
    def get_instance(cls, param):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(param)
        else:
            cls._instance.input = param
        return cls._instance
