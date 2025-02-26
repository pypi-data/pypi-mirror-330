from importlib import import_module
from typing import Callable

_functions = {}


def get_or_create_fnc(fnc: str) -> Callable:
    """Get or create function."""
    if fnc not in _functions:
        name, package = fnc.rsplit(".", 1)
        module = import_module(name)
        _functions[fnc] = getattr(module, package)
    return _functions[fnc]
