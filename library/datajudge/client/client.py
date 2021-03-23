"""Client definition module."""

from __future__ import annotations

import typing
from typing import Any, Optional

from slugify import slugify  # pylint: disable=import-error

from datajudge.utils.constants import (ARTIFACT_STORE_PARAMS, EXP_NAME,
                                       METADATA_STORE_PARAMS, PROJ_ID)
from datajudge.utils.factories import get_stores, select_run_flavour

# For type checking -> avoids circular imports
if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run import Run


class Client:
    """Client class.

    Attributes
    ----------
    project_id :
        The id of the project, needed for the rest metadata store.
    experiment_name :
        Experiment name. An experiment is a logical unit for keeping
        together the validation runs made on a Data Package/Data Resource.
    metadata_params :
        A dictionary containing two keys:
            'store_uri', a uri string pointing to the metadata store
            'credentials', a dictionary with access credentials.
        By default 'store_uri' point to local './validruns' and
        'credentials' is None.
    artifact_params :
        A dictionary containing two keys:
            'store_uri', a uri string pointing to the artifact store
            'credentials', a dictionary with access credentials.
        By default 'store_uri' point to local './validruns' and
        'credentials' is None.

    Methods
    -------
    create_run :
        Create a run for a specific validation framework.

    """

    def __init__(self,
                 project_id: Optional[str] = PROJ_ID,
                 experiment_name: Optional[str] = EXP_NAME,
                 metadata_params: Optional[dict] = None,
                 artifact_params: Optional[dict] = None,
                 ) -> None:

        self._project_id = project_id
        self._experiment_name = experiment_name
        self._experiment_id = slugify(experiment_name,
                                      max_length=20,
                                      separator="_")

        # Because of mutable default args
        if not metadata_params:
            metadata_params = METADATA_STORE_PARAMS
        if not artifact_params:
            artifact_params = ARTIFACT_STORE_PARAMS

        self._metadata_store, self._artifact_store = get_stores(self._experiment_id,
                                                                self._project_id,
                                                                metadata_params,
                                                                artifact_params)

    def create_run(self,
                   data_resource: DataResource,
                   validation_library: str,
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """Create a new run.

        Parameters
        ----------
        validation_library :
            Name of the validation framework used to perform
            the validation task. Used to select a specific
            Run object.
        run_id :
            Optional string parameter for the run id.
        overwrite :
            If True, the run metadata/artifact can be overwritten
            by a run with the same id.

        Return
        ------
        Return a specific Run object.

        """

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
