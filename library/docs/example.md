# Example usage

The first step is to import the library.

```python
import datajudge as dj
```

We instantiate a `DataResource` object which represents some input data. The only mandatory parameter is the `path` that points to the data, but it is recommended to provide as much information as possible to the resource (e.g. name, description, etc.).

```python
PATH_DATA = path/to/data.csv
PATH_SCHEMA = path/to/val-schema.json
NAME = "Example Data"
DESC = "Example dataset used to show a datajudge validation run."

data = dj.DataResource(PATH_DATA,
                       schema=PATH_SCHEMA,
                       name=NAME,
                       description=DESC)
```

We then instantiate a `Client` object. With a `Client` we can interact with the storagesa and create `Run`.
We can provide an `experment_name` parameter to the constructor.

```python
EXP_NAME = "example_experiment"

client = dj.Client(experiment_name=EXP_NAME)
```

By default, the `Client` uses the local filesystem as storage. Specifically, the library will save its output in the "./djruns" directory.

We can now create a `Run` object. In this example, every `Run` created with the client will be organized under the experiment *example_experiment*.
The run requires two mandatory parameters, `data_resource` and `validation_library`.

```python
run = client.create_run(data, "frictionless")
```

The first parameter is a `DataResource` object, the second is a `str` indicating the name of the desired validation framework.
We can use the `Run` as *context manager*. First, we log the *Data Resource*:

```python
with run:
    run.log_data_resource()
```

*Datajudge* make in the background some inference on data and update the *Data Resource* object with information like file extension, hashing, media type, etc.

When we log the short report, the library executes the validation process with `fricionless` method `validate_resource`.

```python
    run.log_short_report()
```

Then we can log a schematic version of the data schema ...

```python
    run.log_short_schema()
```

... and a short and anonymized version of the report produced by `pandas_profiling`.

```python
    run.log_profile()
```

In addition to metadata, we can also persist artifacts. *Datajudge* offers some shortcuts for persisting different types of artifact:

- `persist_data`
  - Save the input data (data + validation scheme)
- `persist_full_report`
  - Save complete validation report produced by a validation framework.
- `persist_inferred_schema`
  - Save inferred schema produced by a validation framework.
- `persist_profile`
  - Save report produced by `pandas_profiling`, both in JSON and HTML format.

```python
    run.persist_data()

    run.persist_full_report()

    run.persist_inferred_schema()

    run.persist_profile()
```