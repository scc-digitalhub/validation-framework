"""Client definition module."""

from __future__ import annotations

import typing
from typing import Any, Optional

from slugify import slugify

from datajudge.utils.constants import ClientDefault
from datajudge.utils.factories import get_stores, select_run_flavour

# For type checking -> avoids circular imports
if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run import Run


class Client:
    """Client class."""

    def __init__(self,
                 project_id: Optional[str] = ClientDefault.PROJ_ID.value,
                 experiment_name: Optional[str] = ClientDefault.EXP_NAME.value,
                 metadata_store_uri: Optional[str] = ClientDefault.STORE_URI.value,
                 artifact_store_uri: Optional[str] = ClientDefault.STORE_URI.value,
                 credentials: Optional[dict] = ClientDefault.CREDENTIALS.value) -> None:

        self._project_id = project_id
        self._experiment_name = experiment_name
        self._experiment_id = slugify(experiment_name,
                                      max_length=20,
                                      separator="_")
        self._metadata_store, self._artifact_store = get_stores(self._experiment_id,
                                                                self._project_id,
                                                                metadata_store_uri,
                                                                artifact_store_uri,
                                                                credentials)

    def create_run(self,
                   data_resource: DataResource,
                   validation_library: str,
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = True) -> Run:
        """Create a new run."""

        run_id = self._metadata_store.get_run_id(run_id)

        self._metadata_store.create_run_enviroment(run_id, overwrite=overwrite)

        run_metadata_uri = self._metadata_store.get_run_metadata_uri(run_id)
        data_resource_uri = self._metadata_store.get_data_resource_uri(run_id)
        run_artifacts_uri = self._artifact_store.get_run_artifacts_uri(run_id)

        run_builder_args = (self._experiment_name,
                            self._experiment_id,
                            run_id,
                            run_metadata_uri,
                            run_artifacts_uri,
                            data_resource_uri)

        run = select_run_flavour(run_builder_args,
                                 validation_library,
                                 data_resource,
                                 self)

        return run

    def _persist_metadata(self,
                          src: dict,
                          dst: str,
                          src_type: str) -> None:
        """Persist metadata."""
        self._metadata_store.persist_metadata(src,
                                              dst,
                                              src_type)

    def _persist_artifact(self,
                          src: Any,
                          dst: str,
                          src_name: Optional[str] = None) -> None:
        """Persist artifact."""
        self._artifact_store.persist_artifact(src, dst, src_name)

    def __repr__(self) -> str:
        return str(self.__dict__)
