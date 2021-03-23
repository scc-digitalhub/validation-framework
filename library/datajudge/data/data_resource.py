from typing import List, Mapping, Optional, Union


class DataResource:
    """DataResource object as decribed in
    frictionless Data Resource specification.

    Attributes
    ----------
    uri_data :
        Required. An URI (or a list of URI) that point to
        data to be validated.
    uri_schema :
       An URI pointing to a validation schema.
    name :
        Name of the Data Resource.
    title :
        A title or label for the resource.
    description :
        A description of the resource.
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
                 uri_data: Union[str, list],
                 uri_schema: Optional[str] = None,
                 name: Optional[str] = None,
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 sources: Optional[List[Mapping]] = None,
                 licenses: Optional[List[Mapping]] = None) -> None:
        self.path = uri_data
        self.name = name
        self.profile = None
        self.title = title
        self.description = description
        self.format = None
        self.mediatype = None
        self.encoding = None
        self.bytes = None
        self.hash = None
        self.schema = uri_schema
        self.sources = sources
        self.licenses = licenses

    def to_dict(self):
        """Return dictionary of non null values."""
        #return {k: v for k, v in self.__dict__.items() if v is not None}
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
