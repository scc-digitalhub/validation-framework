# Run

A `Run` is a data validation/profiling process executed in a defined organizational context (called `experiment`) and performed by some validation framework.
The `Run` object is  created by a `Client` and can perform various tasks:

- Log descriptive metadata
- Persist artifacts
- Fetch input data from the backend
- Start validation/profiling process

The `Run` wraps some methods exposed by validation frameworks. *Datajudge* can support different validation libraries. At the moment we have implemented a plugin for `frictionless`.
To create a `Run`, we need to instantiate a `Client` and a `DataResource`.

```python
import datajudge as dj

client = dj.Client()
data = dj.DataResource("path/to/data")

```

The run can be initialized with `Client.create_run` method. The parameters required are:

- A `DataResource` object
- A `str` describing the validation framework to use.

The method `create_run` accepts also other two keywords arguments:

- `run_id`, specify the ID of the run
- `overwrite`, if there is already a run with the specified ID, enable the overwriting of all metadata tied to that run

```python

run = client.create_run(data,
                        "frictionless",
                        run_id="some_str_id",
                        overwrite=True)

```

You can use the `Run` as context manager ...

```python

with run:
    # SOME CODE

```

... or not.

```python

run.some_method()

```

Note that if the `Run` is used outside the context manager, some metadata will not be updated in the `run_metadata` output.
The `Run` object is flexible. You can perform validations directly with it ...

```python

run = client.create_run(data, "frictionless")

with run:
    
    # The validation process is started automatically
    run.log_short_report()
    run.persist_report()

    # or manually
    report = run.validate_resource()
    run.log_short_report(report)
    run.persist_report(report)

```

... or use it only to handle metadata logging and artifacts fetching/persistence, leaving the management of the validation process to a third-party framework. For this specific scenario, you could use a *generic* run.

```python
from frictionless import validate_resource, Schema, Resource

run = client.create_run(data, "generic")

with run:

    # Fetch input data/validation schema
    path_data = run.fetch_input_data()
    path_schema = run.fetch_validation_schema()

    # Create a frictionless resource and schema
    resource = Resource(path_data)
    schema = Schema(path_schema)
    
    # Validate with frictionless
    report = validate_resource(resource, schema=schema)

    # Use run method to log/persist report
    run.log_short_report(report)
    run.persist_report(report)

```
