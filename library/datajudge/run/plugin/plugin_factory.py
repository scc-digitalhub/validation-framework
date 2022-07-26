"""
Plugin builder factory module.
"""
from __future__ import annotations

import typing
from typing import List

from datajudge.run.plugin.registry import REGISTRY

if typing.TYPE_CHECKING:
    from datajudge.utils.config import ExecConfig


def builder_factory(config: List[ExecConfig],
                    typology: str,
                    stores: dict
                    ) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config:
        try:
            builders.append(REGISTRY[typology][cfg.library](stores,
                                                            cfg.fetchMode,
                                                            cfg.readerArgs,
                                                            cfg.execArgs))
        except KeyError:
            raise NotImplementedError
    return builders
