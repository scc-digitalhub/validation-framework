# Profiling

The profiling process is the process where a framework try to profile a `DataResource`.

## Library supported

- `frictionless`
- `pandas_profiling`

## Run methods

```python
import datajudge as dj

# Creating run ...

with run:

    run.profile()
    run.profile_wrapper()
    run.profile_datajudge()
    run.log_profile()
    run.persist_profile()


```

### Execution methods

Execution method tell plugings to execute profiling over a resource. All this methods accept specific framework arguments as argument.

- `run.profile()`, execute both framework profiling and datajudge profile parsing
- `run.profile_wrapper()`, execute only framework profiling, return a specific framework artifact
- `run.profile_datajudge()`, execute both framework profiling and datajudge profile parsing, return a `DatajudgeProfile`

### Data and metadata persistence

- `run.log_profile()`, log `DatajudgeProfile` into the `MetadataStore`
- `run.profile()`, persist artifact into the default `ArtifactStore`
