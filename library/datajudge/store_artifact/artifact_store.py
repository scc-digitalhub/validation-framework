"""
Abstract class for artifact store.
"""
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from datajudge.utils.uri_utils import rebuild_uri
from datajudge.utils.utils import LOGGER


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


class ArtifactStore:
    """
    Abstract artifact class that defines methods to persist/fetch
    artifacts into/from different storage backends.

    Attributes
    ----------
    name : str
        Name of store.
    artifact_uri : str
        An URI string that points to the storage.
    temp_dir : str
        Temporary download path.
    config : dict, default = None
        A dictionary with the credentials/configurations
        for the backend storage.

    Methods
    -------
    persist_artifact :
        Method to persist an artifact.
    fetch_artifact :
        Method to fetch an artifact.
    get_run_artifacts_uri :
        Return the URI of the artifact store for the Run.

    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 name: str,
                 artifact_uri: str,
                 temp_dir: str,
                 config: Optional[dict] = None
                 ) -> None:
        self.name = name
        self.artifact_uri = artifact_uri
        self.temp_dir = temp_dir
        self.config = config
        self.resource_paths = ResourceRegistry()

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

    def fetch_artifact(self,
                       src: str,
                       file_format: str) -> str:
        """
        Method to fetch an artifact and return the temporary
        path where it is stored.
        """
        tmp_path = self.get_resource(f"{src}_{file_format}")
        if tmp_path is not None:
            return tmp_path
        LOGGER.info(f"Fetching resource {src} from store {self.name}")
        return self._get_and_register_artifact(src, file_format)

    @abstractmethod
    def _get_and_register_artifact(self,
                                   src: str,
                                   file_format: str) -> str:
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

    def get_resource(self, key: str) -> str:
        """
        Method to return temporary path of a registered resource.
        """
        return self.resource_paths.get_resource(key)

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
