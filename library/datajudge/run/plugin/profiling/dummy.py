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
                profiler_kwargs: Optional[dict] = None
                ) -> dict:
        """
        Generate dummy profile.
        """
        profile = self.registry.get_result(res_name)
        if profile is not None:
            return profile
        profile = {}
        self.registry.add_result(res_name, profile)
        return profile

    def render_artifact(self, obj: Any) -> List[tuple]:
        """
        Return a dummy profile to be persisted as artifact.
        """
        profile = dict()
        filename = self._fn_profile.format("dummy.json")
        return [self.get_render_tuple(profile, filename)]
