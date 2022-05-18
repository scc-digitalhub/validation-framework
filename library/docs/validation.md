# Validation

The validation process is the process where a framework validate one or more `DataResource` in accordance to a given `Constraint`.

## Run methods

```python
import datajudge as dj

# Creating run ...

with run:

    run.validate()
    run.validate_wrapper()
    run.validate_datajudge()
    run.log_report()
    run.persist_report()
```

### Execution methods

Execution method tell plugings to execute validation over a resource. All this methods accept specific framework arguments as argument and a list of `Constraint` to validate.

- `run.validate()`, execute both framework validation and datajudge report parsing
- `run.validate_wrapper()`, execute only framework validation, return a specific framework artifact
- `run.validate_datajudge()`, execute both framework validation and datajudge report parsing, return a `DatajudgeReport`

### Data and metadata persistence

- `run.log_report()`, log `DatajudgeReport` into the `MetadataStore`
- `run.validate()`, persist artifact into the default `ArtifactStore`

## Library supported

- `frictionless`

```python
run_config = {

    # The only parameter accepted is "frictionless"
    "library": "frictionless",

    # execArgs accepted are the ones passed to the method validate()
    "execArgs": {},

    # This arguments is related more to the stores than the run plugins,
    # but in general, to perform a better validation with frictionless,
    # a csv format is better
    "tmpFormat": "csv"
}
```

- `duckdb`

```python
run_config = {

    # The only parameter accepted is "duckdb"
    "library": "duckdb",

    # There are no suitable execution arguments for the duckdb validator
    "execArgs": {},

    # This arguments is related more to the stores than the run plugins
    "tmpFormat": "csv" or "parquet"
}
```
