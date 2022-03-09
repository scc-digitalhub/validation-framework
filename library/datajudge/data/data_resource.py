"""
DataResource module.
"""
from typing import Optional, Union


class DataResource:
    """
    Oobject that represents a resource.

    Attributes
    ----------
    name : str
        Name of the Data Resource.
    path : str
        An URI (or a list of URI) that point to data.
    store : str
        Store name where to find the resource.
    package : str, default = None
        Package name that Resource belongs to.
    title : str, default = None
        Human readable name for the resource.
    description : str, default = None
        A description of the resource.

    Methods
    -------
    dict :
        Transform the object in a dictionary.

    """

    def __init__(self,
                 path: Union[str, list],
                 name: str,
                 store: Optional[str] = None,
                 package: Optional[str] = None,
                 title: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        self.path = path
        self.name = name
        self.store = store
        self.package = package
        self.title = title
        self.description = description
        self.tmp_pth = None

    def dict(self) -> dict:
        """
        Return dictionary of non null values.
        """
        data = {
            "path": self.path,
            "name": self.name,
            "store": self.store,
            "package": self.package,
            "title": self.title,
            "description": self.description
        }
        return data

    def __repr__(self) -> str:
        return str(self.dict())
