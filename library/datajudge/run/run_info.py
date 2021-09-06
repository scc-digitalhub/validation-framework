"""
RunInfo module.
Implementation of the basic Run's metadata.
"""
from datajudge.utils.utils import get_time


# pylint: disable=too-many-instance-attributes,too-many-arguments

class RunInfo:
    """
    Run's metadata.

    Attributes
    ----------
    experiment_id : str
        Id of the experiment.
    experiment_name : str
        Name of the experiment.
    run_id : str
        Run id.
    run_metadata_uri : str
        URI that point to the metadata store.
    run_artifacts_uri : str
        URI that point to the artifact store.
    data_resource_uri : str
        URI that point to the resource.

    Methods
    -------
    to_dict :
        Transform the object in a dictionary.

    """

    def __init__(self,
                 experiment_name: str,
                 experiment_id: str,
                 run_id: str,
                 run_metadata_uri: str,
                 run_artifacts_uri: str) -> None:

        self.experiment_name = experiment_name
        self.experiment_id = experiment_id

        self.run_id = run_id
        self.run_metadata_uri = run_metadata_uri
        self.run_artifacts_uri = run_artifacts_uri

        self.data_resource_uri = None

        self.validation_library_name = None
        self.validation_library_version = None

        self.profiling_library_name = None
        self.profiling_library_version = None

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
            "experimentId": self.experiment_id,
            "runId": self.run_id,
            "runMetadataUri": self.run_metadata_uri,
            "runArtifactsUri": self.run_artifacts_uri,
            "dataResourceUri": self.data_resource_uri,
            "validationLibraryName": self.validation_library_name,
            "validationLibraryVersion": self.validation_library_version,
            "profilingLibraryName": self.profiling_library_name,
            "profilingLibraryVersion": self.profiling_library_version,
            "created": self.created,
            "beginStatus": self.begin_status,
            "started": self.started,
            "endStatus": self.end_status,
            "finished": self.finished
        }
        return run_dict

    def __repr__(self) -> str:
        return str(self.to_dict())
