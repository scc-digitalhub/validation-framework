"""
Frictionless utils module.
"""
from typing import List, Union

from frictionless import Resource, Detector

from datajudge.utils.config import ConstraintFrictionless


# With bigger buffer/sample we should avoid error encoding detection
custom_frictionless_detector = Detector(buffer_size=20000, sample_size=1250)


def frictionless_schema_converter(
    schema: Union[dict, "Schema"], resource_name: str
) -> List[ConstraintFrictionless]:
    """
    Convert a frictionless schema in a list of ConstraintFrictionless.

    Parameters
    ----------
    schema : Union[dict, Schema]
        A valid frictionless Resource table schema.
    resource_name : str
        Name of the resource.

    Returns
    -------
    List[ConstraintFrictionless]
        A list of ConstraintFrictionless.
    """
    constraints = []
    for field in schema.get("fields", []):
        cnt = 0

        type_ = field.get("type")
        if type_ is not None:
            name = f'{field.get("name", "")}_{str(cnt)}'
            c = ConstraintFrictionless(
                type="frictionless",
                name=name,
                resources=[resource_name],
                title=name,
                field=field.get("name"),
                fieldType=type_,
                constraint="type",
                value=type_,
                weight=5,
            )
            constraints.append(c)
            cnt += 1

        format_ = field.get("format")
        if format_ is not None:
            name = f'{field.get("name", "")}_{str(cnt)}'
            c = ConstraintFrictionless(
                type="frictionless",
                name=name,
                resources=[resource_name],
                title=name,
                field=field.get("name"),
                fieldType=type_,
                constraint="format",
                value=format_,
                weight=5,
            )
            constraints.append(c)
            cnt += 1

        c_list = field.get("constraints", {})
        if c_list:
            for k, v in c_list.items():
                name = f'{field.get("name", "")}_{str(cnt)}'
                c = ConstraintFrictionless(
                    type="frictionless",
                    name=name,
                    resources=[resource_name],
                    title=name,
                    field=field.get("name"),
                    fieldType=type_,
                    constraint=k,
                    value=v,
                    weight=5,
                )
                constraints.append(c)
                cnt += 1

    return constraints


from frictionless import Resource


def describe_resource(pth: str) -> dict:
    """
    Describe a resource using frictionless.
    """
    desc = Resource.describe(
        source=pth, expand=True, detector=custom_frictionless_detector
    )
    return desc.to_dict()
