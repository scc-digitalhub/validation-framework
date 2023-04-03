Datajudge usability scenarios
-----------------------------

Frictionless validation scenario
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A possible scenario for using datajudge is to validate tabular datasets following the frictionless-data validation model specification.
Datajudge offers two types of frictionless constraints. In the first case, the user provides a constraint to verify a single rule,
for example a certain data type applied to a field, a format that the data must comply with in a certain field or
a constraint between those provided by frictionless as the maximum value of the integers in a field, etc. In the second case,
the user can provide a table schema that describes a resource as a specific constraint,
thus applying the set of rules to the dataset in a single validation process.


SQL validation on file with DuckDB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With DuckDB validator it is possible to execute SQL validation queries on files. In this scenario, datajudge retrieves the resources from the various backend stores,
saves them as local temporary files and loads the files into a temporary DuckDB database on which the single plugin then executes a validation query specified in the
constraint.


SQL validation with SQLAlchemy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With SQLAlchemy validator it is possible to execute SQL validation queries using the query engine of a deployed database.
In this scenario, datajudge retrieves resources specified in the constraint using directly the database query engine of the databese where
the physical resources are stored. The SQLAlchemy validator only execute validation on local/remote database storages.


Validation and metrics with great-expectations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another scenario is the one which leverages the capabilieties of great-expectations. The great-expectations constraints apply an expectation to the resources
as descibed by the framework documentation
