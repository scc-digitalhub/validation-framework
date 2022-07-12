
Data Resource
=============

A ``DataResource`` is a representation of a pyhisical resource.

To create a validation run, you must instantiate at least one ``DataResource`` object. A basic ``DataResource`` must have a name, a path to the input data and a refernce to the store where it can be retrieved.

.. code-block:: python

   import datajudge as dj

   STORE = dj.StoreConfig(name="store-name",
                          type="type",
                          uri="uri",
                          isDefault=True)

   RESOURCE = dj.DataResource(path="path-to-data",
                              name="res-name",
                              store="store-name")

The reference to the store implies that a store with that specific name must be instantiated. At runtime, if a run try to fetch a ``DataResource`` from a ``Store`` that is not passed to the ``Client`` constructor, the program will raise a ``StoreError``.

The other parameters are optional, but it's recommended to add them to enrich your data description.

.. code-block:: python

   RESOURCE = dj.DataResource(path="path-to-data",
                              name="res-name",
                              store="store-name",
                              schema="path to a data schema or an embedded schema",
                              package="name of the package to which the resource belongs",
                              title="human readable name",
                              description="description of the resource")
