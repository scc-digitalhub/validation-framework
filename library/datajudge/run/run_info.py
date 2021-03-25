from datajudge.utils.time_utils import get_time


class RunInfo:
    """
    Run's metadata.

    Attributes
    ----------
    experiment_id :
        Id of the experiment.
    experiment_name :
        Name of the experiment.
    run_id :
        Run id.
    run_metadata_uri :
        URI that point to the metadata store.
    run_artifacts_uri :
        URI that point to the artifact store.
    data_resource_uri :
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
                 run_artifacts_uri: str,
                 data_resource_uri: str) -> None:

        self.experiment_name = experiment_name
        self.experiment_id = experiment_id

        self.run_id = run_id
        self.run_metadata_uri = run_metadata_uri
        self.run_artifacts_uri = run_artifacts_uri
        self.data_resource_uri = data_resource_uri

        self.validation_library = ""
        self.library_version = ""

        self.created = get_time()
        self.begin_status = ""
        self.started = ""
        self.end_status = ""
        self.finished = ""

    def to_dict(self):
        """
        Return a dictionary of attributes.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
