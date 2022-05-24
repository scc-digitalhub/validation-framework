"""
Base abstract Run Plugin module.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from __future__ import annotations
from copy import deepcopy

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List
from datajudge.data.data_resource import DataResource

from datajudge.run.plugin.plugin_utils import RenderTuple
from datajudge.utils.exceptions import StoreError
from datajudge.utils.utils import LOGGER, get_uiid

if typing.TYPE_CHECKING:
    from datajudge.run.plugin.plugin_utils import Result
    from datajudge.store_artifact.artifact_store import ArtifactStore


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    def __init__(self) -> None:
        self._id = get_uiid()
        self.lib_name = self.get_lib_name()
        self.lib_version = self.get_lib_version()
        self.logger = LOGGER
        self.multiprocess = False
        self.multithread = False

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        """
        Configure a plugin.
        """

    @abstractmethod
    def execute(self) -> dict:
        """
        Execute main plugin operation.
        """

    @abstractmethod
    def render_datajudge(self, obj: Result) -> Result:
        """
        Produce datajudge output.
        """

    @abstractmethod
    def render_artifact(self, obj: Result) -> Result:
        """
        Render an artifact to be persisted.
        """

    @staticmethod
    def get_render_tuple(obj: Any, filename: str) -> RenderTuple:
        """
        Return a RenderTuple.
        """
        return RenderTuple(obj, filename)

    @staticmethod
    @abstractmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """

    @staticmethod
    @abstractmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """

    def get_library(self) -> dict:
        """
        Get library info.
        """
        return {
            "libraryName": self.get_lib_name(),
            "libraryVersion": self.get_lib_version()
        }


class PluginBuilder:
    """
    Abstract PluginBuilder class.
    """
    def __init__(self,
                 exec_args: dict,
                 file_format: str,
                 stores: List[ArtifactStore]) -> None:
        self.exec_args = exec_args
        self.file_format = file_format
        self.stores = stores

    @abstractmethod
    def build(self, *args, **kwargs) -> List[Plugin]:
        """
        Build a list of plugin.
        """

    def fetch_resource(self,
                       res: DataResource) -> DataResource:
        """
        Fetch resources from storages.
        """
        resource = deepcopy(res)
        for store in self.stores:
            if store.name == resource.store:
                resource.tmp_pth = store.fetch_artifact(resource.path,
                                                        self.file_format)
                return resource
        raise StoreError(f"No store registered with name '{resource.store}'. " +
                         f"Impossible to fetch resource '{resource.name}'")