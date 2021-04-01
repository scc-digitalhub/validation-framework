# Library for validation process monitoring

## Overview

*Datajudge* is a library that produces a set of metadata during the data validation process operated by some validation framework and allows data and reporting persistence as artifacts.

The metadata produced by *Datajudge* are of four types:

- `Run metadata`
  - Describe the validation run. By validation run, we mean a defined validation process executed in a defined organizational context (called experiment).
- `Data Package` / `Data Resource`
  - According to the Frictionless technical    specifications, *Datajudge* produces a descriptor file of the input data.
- `Short Report`
  - The library produces a concise and anonymized version of the report created by the validation framework.
- `Artifact metadata`
  - A series of metadata that associate the artifacts persisted by the user with a run and indicate their location.

*Datajudge* logs this set of metadata into various backends. At the moment, the library supports two types of backends:

- Local filesystem
- *DigitalHub* framework (coming with this repository)

## Installation and requirements

The library supports Python>=3.7

To install the library download the source code or clone the repository.
Change directory to the `library` folder:

```bash
cd library
```

And then install it either with `pip` or `python`

```bash
pip install .
```

or

```bash
python setup.py install
```

## Example usage

The first step is to import the library. We import also packages required for the validation process.

```python
import Datajudge as dj
from frictionless import validate_resource, Schema
```

We instantiate a `DataResource` object. The only mandatory parameter is the `path` that points to the data, but it is recommended to provide as much information as possible to the resource (e.g. name, description, etc.).

```python
PATH_DATA = path/to/data.csv
PATH_SCHEMA = path/to/val-schema.json
NAME = "Example Data Resource"
DESC = "Data Resource to test Datajudge functionalities."

data = dj.DataResource(PATH_DATA,
                       schema=PATH_SCHEMA,
                       name=NAME,
                       description="DESC")
```

We then instantiate a `Client` object. With a client we can:
interact with the storages for metadata and artifacts
create a `Run`

```python
EXP_NAME = "example_experiment"

client = dj.Client(experiment_name=EXP_NAME)
```

By default, the `Client` uses the local filesystem as metadata and artifact store. Specifically, the library will save its output in the "./validruns" directory.

We can now create a `Run` object. In this example, every `Run` created with the client will be organized under the experiment *example_experiment*.
The run requires two mandatory parameters:
`data_resource`
`validation_library`

```python
run = client.create_run(data, "frictionless")
```

The first parameter is a `DataResource` object, the second is a string indicating the name of the desired validation framework. Currently *Datajudge* only supports *frictionless*.

We can use the `Run` with `with` statement. First, we log the *Data Resource*:

```python
with run:

    # Log data resource
    run.log_data_resource()
```

*Datajudge* make in the background some inference on data and update the *Data Resource* object with information like file extension, hashing, media type, etc.

We execute the validation process with *fricionless* APIs ...

```python
    # Validation
    report = validate_resource(run.get_resource(schema=Schema(data.schema)))
```

 ... and log the short report.

```python
    # Log short report
    run.log_short_report(report)
```

In addition to metadata, we can also persist artifacts. *Datajudge* offers some shortcuts for persisting different types of artifact:

- `persist_data()`
  - Save the input data (data + validation scheme)
- `persist_full_report(report)`
  - Save complete report
  - It requires the report produced by the validation framework as a parameter
- `persist_inferred_schema(schema)`
  - Save inferred schema
  - It requires the inferred schema produced by the validation framework as a parameter

```python
    # Persist input data (data + validation schema)
    run.persist_data()

    # Persist full report as artifact
    run.persist_full_report(report)

    # Persist inferred schema
    resource = run.get_resource()
    resource.infer()
    schema_infer = resource["schema"]
    run.persist_inferred_schema(schema_infer)
```

The run metadata are logged autonomously in the background by the library.
