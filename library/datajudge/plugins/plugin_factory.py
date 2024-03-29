"""
Plugin builder factory module.
"""
from typing import List

from datajudge.plugins.registry import REGISTRY


def builder_factory(config: List["ExecConfig"], typology: str, stores: dict) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config:
        try:
            builders.append(REGISTRY[typology][cfg.library](stores, cfg.execArgs))
        except KeyError:
            raise NotImplementedError
    return builders
