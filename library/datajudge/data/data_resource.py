from typing import List, Mapping, Optional, Union


class DataResource:
    """
    DataResource object as described in frictionless
    Data Resource specification.

    Attributes
    ----------
    path :
        Required. An URI (or a list of URI) that point to
        data to be validated.
    name :
        Name of the Data Resource.
    profile :
        A string identifying the profile of this descriptor
        as per the profiles specification e.g. 'tabular-data-resource'.
        Inferred.
    title :
        A title or label for the resource.
    description :
        A description of the resource.
    format :
        Standard file extension.
        Inferred.
    mediatype :
        The mediatype/mimetype of the resource e.g. 'text/csv'.
        Inferred.
    encoding :
        Character encoding of the resource’s data file.
        Inferred.
    bytes :
        Size of the file in bytes.
        Inferred.
    hash :
        MD5 hash for this resource.
        Inferred.
    schema :
        An URI pointing to a validation schema.
    sources :
        Source of data.
    licenses :
        Licenses pending on data.

    Methods
    -------
    to_dict :
        Transform the object in a dictionary.

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

    def to_dict(self) -> dict:
        """
        Return dictionary of non null values.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}
        # return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
