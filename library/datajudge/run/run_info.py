"""
RunInfo module.
Implementation of the basic Run's metadata.
"""
from datajudge.utils.time_utils import get_time


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

        self.validation_library = None
        self.library_version = None

        self.created = get_time()
        self.begin_status = None
        self.started = None
        self.end_status = None
        self.finished = None

    def to_dict(self) -> dict:
        """
        Return a dictionary of attributes.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
