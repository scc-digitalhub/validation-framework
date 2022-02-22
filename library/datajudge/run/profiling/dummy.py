"""
Dummy implementation of profiling plugin.
"""
# pylint: disable=import-error,invalid-name
from typing import Any, List, Optional

from datajudge.run.profiling.profiling_plugin import (ProfileTuple,
                                                      Profiling,
                                                      RenderTuple)


FN_PROFILE_JSON = "profile_dummy.json"


class ProfilePluginDummy(Profiling):
    """
    Dummy implementation of profiling plugin.
    """

    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.lib_name = None
        self.lib_version = None

    def parse_profile(self,
                      profile: Any,
                      res_name: str) -> ProfileTuple:
        """
        Return none.
        """
        return ProfileTuple(None, {}, {})

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
        self.registry.add_result(res_name, profile, None)
        return profile

    def render_object(self, obj: Any) -> List[RenderTuple]:
        """
        Return a dummy profile to be persisted as artifact.
        """
        return [RenderTuple({}, FN_PROFILE_JSON)]
