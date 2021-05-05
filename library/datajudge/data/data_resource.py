"""
DataResource module.
Implementation of a DataResource object as defined in frictionless
specifications.
"""
from typing import List, Mapping, Optional, Union

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments


class DataResource:
    """
    DataResource object as described in frictionless Data Resource
    specifications.

    A Data Resource must have a path pointing to it's locations.
    It's strongly advised to fill the other fields to better describe
    the Data Resource.
    For more info, please check:
    'https://specs.frictionlessdata.io/data-resource/'

    Attributes
    ----------
    path : str
        Required. An URI (or a list of URI) that point to data.
    name : str, default = None
        Name of the Data Resource.
    title : str, default = None
        A title or label for the resource.
    description : str, default = None
        A description of the resource.
    schema : str, default = None
        An URI pointing to a validation schema.
    sources : list of dict, default = None
        Source of data.
    licenses : list of dict, default = None
        Licenses pending on data.

    Methods
    -------
    to_dict :
        Transform the object in a dictionary.

    get_metadata :
        Return some metadata to attach to artifacts.

    Notes
    -----
    The following attributes are inferred by the validation framework.
    profile : str, default = None
        A string identifying the profile of Data Resource descriptor
        as per the profiles specification e.g. 'tabular-data-resource'.
    format : str, default = None
        Standard file extension.
    mediatype : str, default = None
        The mediatype/mimetype of the resource e.g. 'text/csv'.
    encoding : str, default = None
        Character encoding of the resource’s data file.
    bytes : int, default = None
        Size of the file(s) in bytes.
    hash : str, default = None
        MD5 hash for this resource.

    """

    def __init__(self,
                 path: Union[str, list],
                 schema: Optional[str] = None,
                 name: Optional[str] = None,
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 sources: Optional[List[Mapping]] = None,
                 licenses: Optional[List[Mapping]] = None) -> None:
        self.path = path
        self.name = name
        self.profile = None
        self.title = title
        self.description = description
        self.format = None
        self.mediatype = None
        self.encoding = None
        self.bytes = None
        self.hash = None
        self.schema = schema
        self.sources = sources
        self.licenses = licenses

    def get_metadata(self) -> dict:
        """
        Return metadata for artifacts.
        """
        base = {
            "name": self.name,
            "profile": self.profile,
            "title": self.title,
            "mediatype": self.mediatype,
            "encoding": self.encoding
        }
        metadata = {
            k: v for k, v in base.items() if v is not None
        }
        return metadata

    def to_dict(self) -> dict:
        """
        Return dictionary of non null values.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}
        # return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
