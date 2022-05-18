# Constraints

A `Constraint` is a rule that resource must fit to be considered valid. You can define as many `Constraint` as you want, and *datajudge* will parse them and pass to the desired framework of validation.
We now support two validation framework, `frictionless` and `duckdb`.

`Constraint`s share the following parameters

- *name*, identifier for the constraint
- *title*, optional, human readable version of the identifier
- *resources*, targeted LIST of resources
- *weight*, optional, importance of an eventual error

## Frictionless constraint

`frictionless` uses a `table_schema` to validate a resource. We do not accept `table_schemas`, instead we pass to the framework one or more contraints.
The parameters to define a `ConstraintsFrictionless` are the following:

- *type*, MUST be "frictionless"
- *field*, specified targeted field
- *fieldType*, specified targeted field type
- *constraint*, frictionless constraint
  - *format*
  - *type*
  - *required*
  - *unique*
  - *minLength*
  - *maxLength*
  - *minimum*
  - *maximum*
  - *pattern*
  - *enum*
- *value*, value expeted

Example:

```python
import datajudge as dj

# Artifact Store
STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                type="local",
                                uri="./djruns",
                                isDefault=True)


# Data Resource
RES_LOCAL_01 = dj.DataResource(path="path-to-data",
                               name="example-resource",
                               store="local")


# Example constraint. We expect that the values of the
#  specified field have a maximum lenght of 11 characters.
CONSTRAINT_01 = dj.ConstraintsFrictionless(type="frictionless",
                                           title="Example frictionless constraint",
                                           name="example-const",
                                           resources=["example-resource"],
                                           field="field-to-validate",
                                           fieldType="string",
                                           constraint="maxLength",
                                           value=11,
                                           weight=5)
```

## DuckDB constraint

The parameters to define a `ConstraintsDuckDB` are the following:

- *type*, MUST be "duckdb"
- *query*, an SQL query that will be executed on the resources
  - Please note that the query require some precautions
    - When you select from a resource, the resource must be written lowercase
    - The name of the resource where you select from must be in the list of resources passed to the constraint
- *expect*, expected tipology of result
  - *empty*
  - *non-empty*
  - *exact*
  - *range*
  - *minimum*
  - *maximum*
- *value*, value expected
  - Please note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows
    - "(num1, num2)" upper exclusive, lower exclusive
    - "(num1, num2]" upper exclusive, lower inclusive
    - "[num1, num2)" upper inclusive, lower exclusive
    - "[num1, num2]" upper inclusive, lower inclusive
- *check*, tipology of result to evaluate
  - *rows* check number of rows
  - *value* check a single value, e.g. a *select count(\*)*

```python
import datajudge as dj

# Artifact Store
STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                type="local",
                                uri="./djruns",
                                isDefault=True)


# Data Resource
RES_LOCAL_01 = dj.DataResource(path="path-to-data",
                               name="example-resource",
                               store="local")


# Example constraint. We expect that the reesource is not empty.
CONSTRAINT_01 = dj.ConstraintsDuckdb(type="duckdb",
                                     title="Example duckdb constraint",
                                     name="example-const",
                                     resources=["example-resource"],
                                     query="select * from exampl-resource"
                                     expect="non-empty",
                                     check="rows"
                                     weight=5)
```
