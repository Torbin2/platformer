from __future__ import annotations

# import importlib.util
import sys
import json
import pygame

TO_RUN_MODULE = 'main'
THIS_NAME = 'launcher'

if THIS_NAME not in sys.modules:
    __import__(THIS_NAME)

    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    this_module = sys.modules[THIS_NAME]
    sys.modules['pygame'] = this_module

    print(f'injected, running {TO_RUN_MODULE}')
    __import__(TO_RUN_MODULE)


log_file = open('rec.pg', 'w')


def _getattr(module, item, name=''):
    item = name + '.' + item if name else item
    # print(f"get: '{item}'")
    if type(module) is int:
        return module
    return Module(module, item)


class Module:
    def __init__(self, module: Module, name: str):
        self.module = module
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.module(*args, **kwargs)

    def __getattr__(self, item):
        r = getattr(self.module, item)
        return _getattr(r, item, self.name)


def __getattr__(name):
    return _getattr(getattr(pygame, name), name)
