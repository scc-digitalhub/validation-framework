"""
Abstract class for artifact store.
"""
from abc import ABCMeta, abstractmethod
from typing import IO, Any, Optional, Union

from datajudge.utils.commons import (DATAREADER_BUFFER, DATAREADER_FILE,
                                     DATAREADER_NATIVE)
from datajudge.utils.logger import LOGGER
from datajudge.utils.uri_utils import rebuild_uri


class ResourceRegistry:
    """
    Generic registry object to keep track of resources.
    """

    def __init__(self) -> None:
        self.registry = {}

    def register(self,
                 res_name: str,
                 tmp_path: str) -> None:
        """
        Register a resource temporary path.
        """
        if res_name not in self.registry:
            self.registry[res_name] = tmp_path

    def get_resource(self, res_name: str) -> str:
        """
        Return resource temporary path.
        """
        try:
            return self.registry[res_name]
        except KeyError:
            return None

    def clean_all(self) -> None:
        """
        Remove resource from registry.
        """
        self.registry = {}


class ArtifactStore(metaclass=ABCMeta):
    """
    Abstract artifact class that defines methods to persist/fetch
    artifacts into/from different storage backends.

    Attributes
    ----------
    name : str
        Name of store.
    type : str
        Type of store, e.g. s3, sql, local.
    artifact_uri : str
        An URI string that points to the storage.
    temp_dir : str
        Temporary download path.
    config : dict, default = None
        A dictionary with the credentials/configurations
        for the backend storage.

    """

    FILE = DATAREADER_FILE
    NATIVE = DATAREADER_NATIVE
    BUFFER = DATAREADER_BUFFER

    def __init__(self,
                 name: str,
                 store_type: str,
                 artifact_uri: str,
                 temp_dir: str,
                 config: Optional[dict] = None,
                 is_default=False
                 ) -> None:
        self.name = name
        self.store_type = store_type
        self.artifact_uri = artifact_uri
        self.temp_dir = temp_dir
        self.config = config
        self.is_default = is_default
        self.resource_paths = ResourceRegistry()
        self.logger = LOGGER

    @abstractmethod
    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Method to persist an artifact.
        """

    def fetch_file(self,
                   src: str) -> str:
        """
        Return the temporary path where a resource it is stored.
        """
        return (self._get_resource(f"{src}_{self.FILE}") or
                self._get_and_register_artifact(src, self.FILE))

    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.
        """
        return (self._get_resource(f"{src}_{self.NATIVE}") or
                self._get_and_register_artifact(src, self.NATIVE))

    def fetch_buffer(self, src: str) -> IO:
        """
        Return a buffered resource.
        """
        return (self._get_resource(f"{src}_{self.BUFFER}") or
                self._get_and_register_artifact(src, self.BUFFER))

    @abstractmethod
    def _get_and_register_artifact(self,
                                   src: str,
                                   fetch_mode: str
                                   ) -> str:
        """
        Method to fetch an artifact from the backend an to register
        it on the paths registry.
        """

    @abstractmethod
    def _get_data(self, *args) -> Any:
        """
        Method that retrieve data from a storage.
        """

    @abstractmethod
    def _store_data(self, *args) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """

    @abstractmethod
    def _check_access_to_storage(self) -> None:
        """
        Check if there is access to the storage.
        """

    def get_run_artifacts_uri(self,
                              exp_name: str,
                              run_id: str) -> str:
        """
        Return the path of the artifact store for the Run.
        """
        return rebuild_uri(self.artifact_uri, exp_name, run_id)

    def _get_resource(self, key: str) -> Union[str, bool]:
        """
        Method to return temporary path of a registered resource.
        """
        res = self.resource_paths.get_resource(key)
        if res is None:
            return False
        return res

    def _register_resource(self, key: str, path: str) -> None:
        """
        Method to register a resource into the path registry.
        """
        self.resource_paths.register(key, path)

    def clean_paths(self) -> None:
        """
        Delete all temporary paths references from stores.
        """
        self.resource_paths.clean_all()
