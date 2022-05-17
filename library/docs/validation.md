# Validation

The validation process is the process where a framework validate one or more `DataResource` in accordance to a given `Constraint`.

## Library supported

- `frictionless`
- `duckdb`

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

Execution method tell plugings to execute validation over a resource. All this methods accept specific framework arguments as argument.

- `run.validate()`, execute both framework validation and datajudge report parsing
- `run.validate_wrapper()`, execute only framework validation, return a specific framework artifact
- `run.validate_datajudge()`, execute both framework validation and datajudge report parsing, return a `DatajudgeReport`

### Data and metadata persistence

- `run.log_report()`, log `DatajudgeReport` into the `MetadataStore`
- `run.validate()`, persist artifact into the default `ArtifactStore`
