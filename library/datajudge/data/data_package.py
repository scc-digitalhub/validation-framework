"""
DataPackage module.
Implementation of a DataPackage object as defined in frictionless
specifications and with datajudge modification.
"""
# pylint: disable=import-error,invalid-name,too-many-arguments
from __future__ import annotations

import typing
from typing import List, Mapping, Optional

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource


class DataPackage:

    def __init__(self,
                 resources: List[DataResource],
                 constraints: Optional[List[Mapping]] = None,
                 name: Optional[str] = None,
                 id: Optional[str] = None,
                 licenses: Optional[List[Mapping]] = None,
                 profile: Optional[str] = None,
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 homepage: Optional[str] = None,
                 version: Optional[str] = None,
                 sources: Optional[List[Mapping]] = None,
                 contributors: Optional[List[Mapping]] = None,
                 keywords: Optional[List[str]] = None,
                 image: Optional[str] = None,
                 created: Optional[str] = None
                 ) -> None:

        self.resources = resources
        self.constraints = constraints
        self.name = name
        self.id = id
        self.licenses = licenses
        self.profile = profile
        self.title = title
        self.description = description
        self.homepage = homepage
        self.version = version
        self.sources = sources
        self.contributors = contributors
        self.keywords = keywords
        self.image = image
        self.created = created

    def to_dict(self) -> dict:
        """
        Return dictionary of non null values.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        return str(self.to_dict())
