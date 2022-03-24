"""
Plugin factory module.
"""
from __future__ import annotations

import typing
from typing import List

from datajudge.run.plugin import (InferenceBuilderDummy,
                                  InferenceBuilderFrictionless,
                                  ProfileBuilderDummy,
                                  ProfileBuilderFrictionless,
                                  ProfileBuilderPandasProfiling,
                                  ValidationBuilderDuckDB,
                                  ValidationBuilderDummy,
                                  ValidationBuilderFrictionless)
from datajudge.utils.commons import (DUCKDB, DUMMY, FRICTIONLESS, INFERENCE,
                                    PROFILING, VALIDATION, PANDAS_PROFILING)

if typing.TYPE_CHECKING:
    from datajudge.utils.config import ExecConfig


REGISTRY = {
    INFERENCE: {
        DUMMY: InferenceBuilderDummy,
        FRICTIONLESS: InferenceBuilderFrictionless,
        },
    VALIDATION: {
        DUMMY: ValidationBuilderDummy,
        DUCKDB: ValidationBuilderDuckDB,
        FRICTIONLESS: ValidationBuilderFrictionless,
        },
    PROFILING: {
        DUMMY: ProfileBuilderDummy,
        FRICTIONLESS: ProfileBuilderFrictionless,
        PANDAS_PROFILING: ProfileBuilderPandasProfiling,
        }
}


def get_builder(config: List[ExecConfig],
                typology: str) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config:
        try:
            builders.append(REGISTRY[typology][cfg.library](cfg.execArgs))
        except KeyError:
            raise NotImplementedError
    return builders
