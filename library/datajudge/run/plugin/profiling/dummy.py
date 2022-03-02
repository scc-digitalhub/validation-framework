"""
Dummy implementation of profiling plugin.
"""
# pylint: disable=import-error,invalid-name
from typing import Any, List, Optional

from datajudge.run.plugin.profiling.profiling_plugin import Profiling


class ProfilePluginDummy(Profiling):
    """
    Dummy implementation of profiling plugin.
    """

    def update_library_info(self) -> None:
        """
        Do nothing.
        """

    def parse_profile(self,
                      profile: Any,
                      res_name: str) -> tuple:
        """
        Return none.
        """
        return self.get_profile_tuple(None, {}, {})

    def validate_profile(self, profile: Any) -> None:
        """
        Do nothing.
        """

    def profile(self,
                res_name: str,
                data_path: str,
                exec_args: dict
                ) -> dict:
        """
        Generate dummy profile.
        """
        return {}

    def get_outcome(self, obj: Any) -> str:
        """
        Return status of the execution.
        """
        return self._VALID_STATUS

    def render_artifact(self, obj: Any) -> List[tuple]:
        """
        Return a dummy profile to be persisted as artifact.
        """
        profile = {}
        filename = self._fn_profile.format("dummy.json")
        return [self.get_render_tuple(profile, filename)]
