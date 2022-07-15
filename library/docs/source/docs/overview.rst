Overview
========

Datajudge is a framework for monitoring and managing data validation and profiling processes.

Running Datajudge produces in-memory objects, deriving from the execution frameworks used
(for example, frictionless reports, pandas profiling data profiles, etc.),
a series of process descriptive metadata and a series of artifacts that can be persisted on various backend storage.

Datajudge uses a run execution model. A user defines an experiment as an organizational unit
and performs one or more runs that are recorded and tracked under the defined experiment.

Datajudge performs validation and profiling operations on physical tabular data resources.

The typical workflow involves the configuration of the resources, of the backend storages in which the resources are saved
(local or remote filesystems, databases and datalakes) and the configuration of the run itself, where the user specifies
the desired operations and the frameworks to be used.
