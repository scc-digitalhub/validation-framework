"""
RunInfo module.
Implementation of the basic Run's metadata.
"""
from typing import List, Optional

from datajudge.utils.utils import get_time


class RunInfo:
    """
    Run's metadata.

    Attributes
    ----------
    experiment_name : str
        Id of the experiment.
    run_id : str
        Run id.
    run_type: str
        Run typology.
    run_metadata_uri : str
        URI that point to the metadata store.
    run_artifacts_uri : str
        URI that point to the artifact store.
    resources_uri : str
        URI that point to the resource.

    Methods
    -------
    to_dict :
        Transform the object in a dictionary.

    """

    def __init__(
        self,
        experiment_name: str,
        resources: List["DataResource"],
        run_id: str,
        run_config: "RunConfig",
        run_metadata_uri: Optional[str] = None,
        run_artifacts_uri: Optional[str] = None,
    ) -> None:
        self.experiment_name = experiment_name
        self.run_id = run_id
        self.run_config = run_config
        self.run_libraries = None
        self.run_metadata_uri = run_metadata_uri
        self.run_artifacts_uri = run_artifacts_uri

        self.resources = resources

        self.created = get_time()
        self.begin_status = None
        self.started = None
        self.end_status = None
        self.finished = None

    def to_dict(self) -> dict:
        """
        Return a dictionary of attributes.
        """
        run_dict = {
            "experimentName": self.experiment_name,
            "runId": self.run_id,
            "runConfig": self.run_config.dict(exclude_none=True),
            "runLibraries": self.run_libraries,
            "runMetadataUri": self.run_metadata_uri,
            "runArtifactsUri": self.run_artifacts_uri,
            "resources": [i.dict(exclude_none=True) for i in self.resources],
            "created": self.created,
            "beginStatus": self.begin_status,
            "started": self.started,
            "endStatus": self.end_status,
            "finished": self.finished,
        }
        return run_dict

    def __repr__(self) -> str:
        return str(self.to_dict())
