from datajudge.utils.config import ConstraintFrictionless
from datajudge.plugins.utils.frictionless_utils import frictionless_schema_converter


def test_frictionless_schema_converter():
    table_schema = {
        "fields": [
            {"name": "f1", "type": "integer", "format": "default"},
            {"name": "f2", "type": "string", "format": "email"},
            {"name": "f3", "type": "date", "format": "%d/%m/%y"},
        ]
    }
    const = frictionless_schema_converter(table_schema, "test")
    list_const = [
        ConstraintFrictionless(
            name="f1_0",
            title="f1_0",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f1",
            fieldType="integer",
            constraint="type",
            value="integer",
        ),
        ConstraintFrictionless(
            name="f1_1",
            title="f1_1",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f1",
            fieldType="integer",
            constraint="format",
            value="default",
        ),
        ConstraintFrictionless(
            name="f2_0",
            title="f2_0",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f2",
            fieldType="string",
            constraint="type",
            value="string",
        ),
        ConstraintFrictionless(
            name="f2_1",
            title="f2_1",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f2",
            fieldType="string",
            constraint="format",
            value="email",
        ),
        ConstraintFrictionless(
            name="f3_0",
            title="f3_0",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f3",
            fieldType="date",
            constraint="type",
            value="date",
        ),
        ConstraintFrictionless(
            name="f3_1",
            title="f3_1",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f3",
            fieldType="date",
            constraint="format",
            value="%d/%m/%y",
        ),
    ]
    assert const == list_const
