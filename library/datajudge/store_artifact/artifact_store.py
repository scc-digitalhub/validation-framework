"""
Abstract class for artifact store.
"""
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

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


class ArtifactStore:
    """
    Abstract artifact class that defines methods to persist
    artifacts into different storage backends.

    Attributes
    ----------
    artifact_uri : str
        An URI string that points to the storage.
    config : dict, default = None
        A dictionary with the credentials/configurations
        for the backend storage.
    data : bool, default = False
        If True, Run uses ArtifactStore only to fetch artifact
        from backend. If False, Run uses ArtifactStore only to
        persist data into the backend.

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
                 artifact_uri: str,
                 temp_dir: str,
                 config: Optional[dict] = None
                 ) -> None:
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

    @abstractmethod
    def fetch_artifact(self, src: str, file_format: str) -> str:
        """
        Method to fetch an artifact.
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

    def clean_paths(self) -> None:
        """
        Delete all temporary paths references from stores.
        """
        self.resource_paths.clean_all()
