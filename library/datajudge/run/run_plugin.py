"""
Run plugins registry module.
"""
from __future__ import annotations

import typing
from typing import Any, Mapping

from datajudge.run.plugin.plugin_factory import get_plugin

if typing.TYPE_CHECKING:
    from datajudge import RunConfig
    


class RunPlugin:
    
    def __init__(self, run_config: RunConfig) -> None:

        self._inference_plugins = get_plugin(run_config.inference,
                                             "inference")
        self._validation_plugins = get_plugin(run_config.validation,
                                      "validation")
        self._profiling_plugins = get_plugin(run_config.profiling,
                                      "profiling")

    @property
    def inf(self) -> Any:
        return self._inference_plugins

    @property
    def val(self) -> Any:
        return self._validation_plugins

    @property
    def pro(self) -> Any:
        return self._profiling_plugins

    def get_info(self) -> dict:
        return {
            "validation": self.val.libraries(),
            "inference": self.inf.libraries(),
            "profiling":self.pro.libraries(),
        }
