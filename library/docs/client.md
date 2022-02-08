# Client

A `Client` allows the user to interact with backend storages and creates runs associated with the same `experiment`.
A basic `Client` can be created this way:

```python
import datajudge as dj

client = dj.Client()

```

When a `Client` object is created, it instantiates three `store` private objects, one for metadata logging, the other two for artifacts fetching/persistence.
The `Client` set by default local filesystem as artifacts/data and metadata storage, and set a default name for the `experiment`. Some storages may require authentication or need a `project` reference. The `Client` accepts parameters for that as follows:

```python
import datajudge as dj

client = dj.Client(project_id="some_id",
                   experiment_title="some_experiment_title",
                   metadata_store_uri=None,
                   metadata_store_config=None,
                   artifact_store_uri=None,
                   artifact_store_config=None,
                   data_store_uri=None,
                   data_store_config=None)

```

Note that the `artifact_store` interact with output artifact storage and the `data_store` with input data.
With a `Client` you can create one or more `Run`.
