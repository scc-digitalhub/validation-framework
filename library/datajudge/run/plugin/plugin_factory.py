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
                                  ValidationBuilderDuckDB,
                                  ValidationBuilderDummy,
                                  ValidationBuilderFrictionless)
from datajudge.utils.commons import (DUCKDB, DUMMY, FRICTIONLESS, OP_INF,
                                    OP_PRO, OP_VAL, PANDAS_PROFILING)

if typing.TYPE_CHECKING:
    from datajudge.utils.config import OpsConfig


REGISTRY = {
    OP_INF: {
        DUMMY: InferenceBuilderDummy,
        FRICTIONLESS: InferenceBuilderFrictionless,
        },
    OP_VAL: {
        DUMMY: ValidationBuilderDummy,
        DUCKDB: ValidationBuilderDuckDB,
        FRICTIONLESS: ValidationBuilderFrictionless,
        },
    OP_PRO: {
        DUMMY: ProfileBuilderDummy,
        FRICTIONLESS: ProfileBuilderFrictionless,
        PANDAS_PROFILING: ProfileBuilderPandasProfiling,
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
