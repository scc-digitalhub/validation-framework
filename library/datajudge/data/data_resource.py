"""
DataResource module.
"""

from typing import Optional, Union


class DataResource:
    """
    Object that represents a resource.

    Attributes
    ----------
    path : Union[str, list]
        An URI (or a list of URI) that point to data.
    name : str
        Name of the Data Resource.
    store : Optional[str], optional
        Store name where to find the resource, by default None
    schema : Optional[dict], optional
        Resource schema, by default None
    package : Optional[str], optional
        Package name that Resource belongs to, by default None
    title : Optional[str], optional
        Human readable name for the resource, by default None
    description : Optional[str], optional
        A description of the resource, by default None

    """

    def __init__(self,
                 path: Union[str, list],
                 name: str,
                 store: Optional[str] = None,
                 schema: Optional[dict] = None,
                 package: Optional[str] = None,
                 title: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        self.path = path
        self.name = name
        self.store = store
        self.schema = schema
        self.package = package
        self.title = title
        self.description = description
        self.tmp_pth = None

    def to_dict(self) -> dict:
        """
        Return a dict.
        """
        data = {
            "path": self.path,
            "name": self.name,
            "store": self.store,
            "schema": self.schema,
            "package": self.package,
            "title": self.title,
            "description": self.description
        }
        return data

    def __repr__(self) -> str:
        return str(self.to_dict())
