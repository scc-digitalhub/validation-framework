"""
Base abstract Run Plugin module.
"""
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from typing import Any, List

from datajudge.data_reader.utils import build_reader
from datajudge.plugins.utils.plugin_utils import RenderTuple
from datajudge.utils.config import DataResource
from datajudge.utils.exceptions import StoreError
from datajudge.utils.logger import LOGGER
from datajudge.utils.utils import get_uiid


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    def __init__(self) -> None:
        self._id = get_uiid()
        self.lib_name = self.get_lib_name()
        self.lib_version = self.get_lib_version()
        self.logger = LOGGER
        self.data_reader = None
        self.exec_args = None
        self.exec_sequential = True
        self.exec_multiprocess = False
        self.exec_multithread = False
        self.exec_distributed = False

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
    def render_datajudge(self, obj: "Result") -> "Result":
        """
        Produce datajudge output.
        """

    @abstractmethod
    def render_artifact(self, obj: "Result") -> "Result":
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
            "libraryVersion": self.get_lib_version(),
        }


class PluginBuilder:
    """
    Abstract PluginBuilder class.
    """

    def __init__(self, stores: List["ArtifactStore"], exec_args: dict) -> None:
        self.stores = stores
        self.exec_args = exec_args

    @abstractmethod
    def build(self, *args, **kwargs) -> List[Plugin]:
        """
        Build a list of plugin.
        """

    @staticmethod
    def _get_resource_deepcopy(resource: DataResource) -> DataResource:
        """
        Return deepcopy of a resource.
        """
        return deepcopy(resource)

    def _get_resource_store(self, resource: DataResource) -> "ArtifactStore":
        """
        Get the resource store.
        """
        try:
            return [store for store in self.stores if store.name == resource.store][0]
        except IndexError:
            raise StoreError(
                f"No store registered with name '{resource.store}'. Impossible to fetch resource '{resource.name}'"
            )

    @staticmethod
    def _get_data_reader(type: str, store: "ArtifactStore") -> "DataReader":
        """
        Get data reader.
        """
        return build_reader(type, store)

    @abstractmethod
    def destroy(self) -> None:
        """
        Destroy builder.
        """
