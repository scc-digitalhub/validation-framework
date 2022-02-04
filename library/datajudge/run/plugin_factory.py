# pylint: disable=import-error,invalid-name
from __future__ import annotations

from typing import Any

from datajudge.run.inference import InferencePluginFrictionless
from datajudge.run.validation import ValidationPluginFrictionless
from datajudge.run.profiling import InferencePluginPandasProfiling
from datajudge.utils import config as cfg


PLUGIN_REGISTRY = {
    "inference": {
        "frictionless": InferencePluginFrictionless
        },
    "validation": {
        "frictionless": ValidationPluginFrictionless
        },
    "profiling": {
        "pandas_profiling": InferencePluginPandasProfiling
        },
    "snapshot": {}
}


def get_plugin(config: dict) -> Any:
    """
    Factory method that returns a run plugin.
    """
    if config is None:
        return
    if config.enabled:   
        try:
            if isinstance(config, cfg.InferenceConfig):
                return PLUGIN_REGISTRY["inference"][config.library]()
            if isinstance(config, cfg.ValidationConfig):
                return PLUGIN_REGISTRY["validation"][config.library]()
            if isinstance(config, cfg.ProfilingConfig):
                return PLUGIN_REGISTRY["profiling"][config.library]()
            if isinstance(config, cfg.SnapshotConfig):
                return PLUGIN_REGISTRY["snapshot"][config.library]()
            raise TypeError("Invalid plugin configuration.")

        except KeyError as k_err:
            raise NotImplementedError from k_err
