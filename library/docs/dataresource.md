# Data Resource

A `DataResource` is a representation of a *Data Resource* as described in [`frictionless`  specification](https://specs.frictionlessdata.io/data-resource/).

To create a validation run, you must instantiate a `DataResource` object. A basic `DataResource` needs at least a path to the input data.

```python
import datajudge as dj

data = dj.DataResource("path/to/data")
```

The other parameters are optional, but it's recommended to add them to enrich your data description.
Note that the `schema` parameters accepts only a path to the validation schema, and not the full schema embedded.

```python
data = dj.DataResource("path/to/data",
                       name="name-of-resource",
                       schema="path/to/schema",
                       description="some-description")
```
