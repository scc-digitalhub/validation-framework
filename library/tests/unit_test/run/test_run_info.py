from datajudge.run.run_info import RunInfo


def test_to_dict(run_empty, local_resource):
    run_info = RunInfo("experiment_name", [local_resource], "run_id", run_empty)
    run_info.created = "..."
    expected_output = {
        "experimentName": "experiment_name",
        "runId": "run_id",
        "runConfig": run_empty.dict(),
        "runLibraries": None,
        "runMetadataUri": None,
        "runArtifactsUri": None,
        "resources": [local_resource.dict(exclude_none=True)],
        "created": "...",
        "beginStatus": None,
        "started": None,
        "endStatus": None,
        "finished": None,
    }
    assert run_info.to_dict() == expected_output
