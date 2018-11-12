from typing import Callable

import importlib


def get_sample_gen_by_name(name: str) -> Callable:
    return getattr(
        importlib.import_module('numpy.random'),
        name
    )
