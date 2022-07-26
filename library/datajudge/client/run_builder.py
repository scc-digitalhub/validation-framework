"""
RunBuilder module.
"""
from __future__ import annotations

import typing
from typing import List, Optional, Union

from datajudge.metadata.data_resource import DataResource
from datajudge.metadata.run_info import RunInfo
from datajudge.run.run import Run
from datajudge.run.run_handler import RunHandler
from datajudge.utils.commons import DEFAULT_EXPERIMENT
from datajudge.utils.config import RunConfig
from datajudge.utils.exceptions import RunError
from datajudge.utils.utils import get_uiid, listify

if typing.TYPE_CHECKING:
    from datajudge.client.store_handler import StoreHandler


class RunBuilder:
    """
    RunBuilder object to initialize and create runs.

    """

    def __init__(self,
                 store_handler: StoreHandler) -> None:
        """
        The RunBuilder recieves a store handler to get stores.
        """
        self._store_handler = store_handler

    def _init_run(self,
                  exp_name: str,
                  run_id: str,
                  overwrite: bool) -> None:
        """
        Initialize run in the metadata store backend.
        """
        store = self._store_handler.get_md_store()
        store.init_run(exp_name, run_id, overwrite)

    def _get_md_uri(self, exp_name: str, run_id: str) -> str:
        """
        Get the metadata URI store location.
        """
        store = self._store_handler.get_md_store()
        return store.get_run_metadata_uri(exp_name, run_id)

    def _get_art_uri(self, exp_name: str, run_id: str) -> str:
        """
        Get the artifacts URI store location. It uses the default store.
        """
        store = self._store_handler.get_def_store()
        return store.get_run_artifacts_uri(exp_name, run_id)

    @staticmethod
    def _check_unique_resource(resources: List[DataResource]) -> None:
        """
        Check that resources have unique names.
        """
        exists = []
        for res in resources:
            if res.name in exists:
                raise RunError(
                    f"Resource with name {res.name} already exists!")
            exists.append(res.name)

    def create_run(self,
                   resources: Union[List[DataResource], DataResource],
                   run_config: RunConfig,
                   experiment: Optional[str] = DEFAULT_EXPERIMENT,
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """
        Create a new run.
        """
        resources = listify(resources)
        self._check_unique_resource(resources)
        run_id = get_uiid(run_id)

        self._init_run(experiment, run_id, overwrite)
        run_md_uri = self._get_md_uri(experiment, run_id)
        run_art_uri = self._get_art_uri(experiment, run_id)

        run_handler = RunHandler(run_config,
                                 self._store_handler)
        run_info = RunInfo(experiment,
                           resources,
                           run_id,
                           run_config,
                           run_md_uri,
                           run_art_uri)
        run = Run(run_info, run_handler, overwrite)
        return run
