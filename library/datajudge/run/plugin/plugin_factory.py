"""
Plugin factory module.
"""
from __future__ import annotations

import typing

from datajudge.run.plugin import (InferenceBuilderDummy,
                                  InferenceBuilderFrictionless,
                                  ProfileBuilderDummy,
                                  ProfileBuilderFrictionless,
                                  ProfileBuilderPandasProfiling,
                                  ValidationBuilderDummy,
                                  ValidationBuilderFrictionless)
from datajudge.utils.config import OP_INF, OP_PRO, OP_VAL

if typing.TYPE_CHECKING:
    from datajudge.utils.config import OpsConfig


REGISTRY = {
    OP_INF: {
        "_dummy": InferenceBuilderDummy,
        "frictionless": InferenceBuilderFrictionless,
        },
    OP_VAL: {
        "_dummy": ValidationBuilderDummy,
        "frictionless": ValidationBuilderFrictionless,
        },
    OP_PRO: {
        "_dummy": ProfileBuilderDummy,
        "frictionless": ProfileBuilderFrictionless,
        "pandas_profiling": ProfileBuilderPandasProfiling,
        }
}


def get_builder(config: OpsConfig,
                typology: str) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    if config.enabled:
        for cfg in config.config:
            try:
                builders.append(REGISTRY[typology][cfg.library](cfg.exec_args))
            except KeyError:
                raise NotImplementedError
        return builders
    return [REGISTRY[typology]["_dummy"]({})]
