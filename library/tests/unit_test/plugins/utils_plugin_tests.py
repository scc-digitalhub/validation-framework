from datajudge.plugins.utils.plugin_utils import RenderTuple, Result
from datajudge.metadata.datajudge_reports import (
    DatajudgeSchema,
    DatajudgeProfile,
    DatajudgeReport,
)
from datajudge.utils.commons import (
    OPERATION_INFERENCE,
    OPERATION_PROFILING,
    OPERATION_VALIDATION,
)


def correct_result(output):
    assert isinstance(output, Result)
    assert output.errors is None
    assert output.status == "finished"
    assert output.artifact is not None


def correct_execute(output):
    correct_result(output)


def correct_render_datajudge(output, op):
    correct_result(output)
    artifact = output.artifact
    if op == OPERATION_INFERENCE:
        assert isinstance(artifact, DatajudgeSchema)
        assert isinstance(artifact.duration, float)
        assert isinstance(artifact.fields, list)
    if op == OPERATION_PROFILING:
        assert isinstance(artifact, DatajudgeProfile)
        assert isinstance(artifact.duration, float)
        assert isinstance(artifact.stats, dict)
        assert isinstance(artifact.fields, dict)
    if op == OPERATION_VALIDATION:
        assert isinstance(artifact, DatajudgeReport)
        assert isinstance(artifact.duration, float)


def correct_render_artifact(output):
    correct_result(output)
    assert isinstance(output.artifact, list)
    assert isinstance(output.artifact[0], RenderTuple)


def incorrect_execute(output):
    assert isinstance(output, Result)
    assert output.errors is not None
    assert output.status == "error"
    assert output.artifact is None


def incorrect_render_datajudge(output, op):
    assert isinstance(output, Result)
    artifact = output.artifact
    if op == OPERATION_INFERENCE:
        assert isinstance(artifact, DatajudgeSchema)
        assert isinstance(artifact.duration, float)
        assert not artifact.fields
    if op == OPERATION_PROFILING:
        assert isinstance(artifact, DatajudgeProfile)
        assert isinstance(artifact.duration, float)
        assert not artifact.stats
        assert not artifact.fields


def incorrect_render_artifact(output):
    assert isinstance(output, Result)
    assert output.artifact is not None
    assert isinstance(output.artifact, list)
    assert isinstance(output.artifact[0], RenderTuple)
    assert "errors" in output.artifact[0].object
