
Client
======

A ``Client`` is an high level interface that allows an user to interact with backend storages and creates runs associated within an ``experiment``.
The simpliest ``Client`` can be created this way:

.. code-block:: python

   import datajudge as dj

   client = dj.Client()

If you instantiate a ``Client`` without providing a store configuration you can create a ``Run``.
However, ``Runs`` created with this client will raise an error if you attempt to execute any kind of operation.
The reason for this is as follows: when you instantiate a ``Client`` without configuring the stores, the ``StoreHandler``,
the component that manages the stores for the ``Client``, creates a generic *dummy* store object both for the metadata and the artifacts handling.
The various operations (e.g. validation process) are executed on some physical ``Resources`` that are stored inside some backend storage.
The generic *dummy* stores are not connected to any physical backend storage, whether remote or local, so they cannot fetch or reference any ``Resource``.
In general, it is likely that a user wants to log or persist the result of a specific operation.
To do this, the user must pass the stores configurations to the ``Client`` constructor (for more information about stores configuration, check the related page).

.. code-block:: python

   import datajudge as dj

   # Metadata Store
   METADATA_STORE = dj.StoreConfig(title="Local Metadata Store",
                                   type="local",
                                   name="local_md",
                                   uri="./djruns")

   # Artifact Store
   STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                   type="local",
                                   uri="./djruns",
                                   isDefault=True)

   client = dj.Client(metadata_store=METADATA_STORE,
                      store=STORE_LOCAL_01)
