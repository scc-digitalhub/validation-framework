from datajudge.run.run_info import RunInfo
from tests.conftest import RES_LOCAL_01, RUN_CFG_EMPTY


def test_to_dict():
    run_info = RunInfo("experiment_name", [RES_LOCAL_01], "run_id", RUN_CFG_EMPTY)
    run_info.created = "..."
    expected_output = {
        "experimentName": "experiment_name",
        "runId": "run_id",
        "runConfig": RUN_CFG_EMPTY.dict(),
        "runLibraries": None,
        "runMetadataUri": None,
        "runArtifactsUri": None,
        "resources": [RES_LOCAL_01.dict(exclude_none=True)],
        "created": "...",
        "beginStatus": None,
        "started": None,
        "endStatus": None,
        "finished": None,
    }
    assert run_info.to_dict() == expected_output
