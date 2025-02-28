import copy
import importlib
from importlib import import_module

from roboherd.cow import RoboCow


def load_cow(module_name: str, attribute: str) -> RoboCow:
    """Loads a cow from module name and attribute"""
    module = import_module(module_name)
    importlib.reload(module)

    cow = getattr(module, attribute)

    return copy.deepcopy(cow)
