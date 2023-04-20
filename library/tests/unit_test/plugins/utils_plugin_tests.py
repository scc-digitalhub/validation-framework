from datajudge.plugins.base_plugin import Plugin
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


def correct_setup(plg):
    assert isinstance(plg, Plugin)
    # Possible attributes of a plugin
    test_attr = [
        "data_reader",
        "resource",
        "exec_args",
        "error_report",
        "constraint",
        "db",
    ]
    for attr in test_attr:
        if hasattr(plg, attr):
            assert getattr(plg, attr) == "test"


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
        assert isinstance(artifact.constraint, dict)
        assert isinstance(artifact.valid, bool)
        assert isinstance(artifact.errors, dict)


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
    if op == OPERATION_VALIDATION:
        assert isinstance(artifact, DatajudgeReport)
        assert isinstance(artifact.duration, float)
        assert not artifact.valid


def incorrect_render_artifact(output):
    assert isinstance(output, Result)
    assert output.artifact is not None
    assert isinstance(output.artifact, list)
    assert isinstance(output.artifact[0], RenderTuple)
    assert "errors" in output.artifact[0].object


def correct_plugin_build(plugins, plg_type):
    assert isinstance(plugins, list)
    assert len(plugins) == 1
    assert isinstance(plugins[0], plg_type)
