"""
BlobLog class.
It represents the metadata logged into the backend.
"""

class BlobLog:
    """
    Object logged to backend.

    Attributes
    ----------
    run_id : str
        Run id.
    experiment_name : str
        Id of the experiment.
    datajudge_version : str
        Version of the library.
    contents : dict, default None
        Blob of metadata to log.

    """

    def __init__(self,
                 run_id: str,
                 experiment_name: str,
                 datajudge_version: str,
                 contents: dict
                 ) -> None:
        self.run_id = run_id
        self.experiment_name = experiment_name
        self.datajudge_version = datajudge_version
        self.contents = contents

    def to_dict(self) -> dict:
        """
        Return a dictionary.
        """
        run_dict = {
            "runId": self.run_id,
            "experimentName": self.experiment_name,
            "datajudgeVersion": self.datajudge_version,
            **self.contents
        }
        return run_dict

    def __repr__(self) -> str:
        return str(self.to_dict())
