
Stores
======

A store is an object that *datajudge* uses to interact with resources, artifacts and metadata.
They can be configured using a specific ``StoreConfig`` object that accepts the following parameters:


* ``name``, required, identifier of the store
* ``type``, required, specific store type to be instantiated
* ``uri``, required, URI location of artifacts/metadata
* ``title``, optional, human readable description for the store
* ``isDefault``, optional, set an ``ArtifactStore`` as the one where artifact are persisted, ignored by ``MetadataStore``
* ``config``, optional, use to configure credentials, please see `Authentication <./authentication.md>`_ documentation for more information

There are two types of store:


* ``MetadataStore``
* ``ArtifactStore``

MetadataStore
-------------

The ``MetadataStore`` is used by the library to log metadata into a specified backend.

Example configuration:

.. code-block:: python

   import datajudge as dj

   METADATA_STORE = dj.StoreConfig(title="Local Metadata Store",
                                   type="local",
                                   name="local_md",
                                   uri="./djruns")

In this case we create a *local* ``MetadataStore`` that will log metadata locally.
``MetadataStore`` supports the following types:


* *local*
* *http* (DigitalHub store)

ArtifactStore
-------------

The ``ArtifactStore`` is used by the library to fetch and persist artifact from various backend. It is configured like a ``MetadataStore``.
If you configure more than one ``ArtifactStore``, at least one must be set as ``isDefault``.
``ArtifactStore`` supports the following types:


* *local*
* *http* (Doesn't support artifact persistence)
* *ftp*
* *s3*
* *azure*
* *sql* (Doesn't support artifact persistence)
* *odbc* (Doesn't support artifact persistence)
