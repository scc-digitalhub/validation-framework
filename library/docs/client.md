# Client

A `Client` is an high level interface that allows an user to interact with backend storages and creates runs associated within an `experiment`.
The simpliest `Client` can be created this way:

```python
import datajudge as dj

client = dj.Client()
```

A `Client` without store configuration can still provides the basic functionality of run creation. However, runs created with this client will raise an error if you attempt to log metadata or persist artifacts.
The reason for this is as follows: when you instantiate a client without configuring the stores, the StoreHandler, the component that manages the stores for the `Client`, creates *dummy* stores. These stores are not connected to any physical storage, whether remote or local.
The runs of a `Client` without store configurations can still perform inference/validation/profiling operations, returning the operational objects in-memory (e.g. assignable to some variables).

Example:

```python
client = dj.Client()
run = client.create_run([resources], run-configuration)

with run:

    # This will work
    inferred_schema, datajudge_schema = run.infer()

    # These will raise a RunError
    run.log_schema()
    run.persist_schema()
```

In general, it is assumed that a user wants to log the result of the validation run and/or persist its artifact.
To do this, the user passes the stores configurations to the `Client` constructor (for more information about stores configuration, check the related page).

```python

# Metadata Store
METADATA_STORE = dj.StoreConfig(title="Local Metadata Store",
                                name="local_md",
                                uri="./djruns")


# Artifact Store
STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                uri="./djruns",
                                isDefault=True)

client = dj.Client(metadata_store=METADATA_STORE,
                   store=STORE_LOCAL_01)

```
