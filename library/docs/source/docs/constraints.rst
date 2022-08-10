
Constraints
===========

A ``Constraint`` is a rule that resource must fit to be considered valid.
You can define as many ``Constraint`` as you want, and *datajudge* will pass them to the desired framework of validation.

``Constraints`` share the following parameters

* *name*, identifier for the constraint
* *title*, optional, human readable version of the identifier
* *resources*, targeted LIST of resources
* *weight*, optional, importance of an eventual error

Constraint types
----------------

* `Frictionless`_
* `Frictionless schema`_
* `DuckDB`_
* `SQLAlchemy`_
* `Great Expectations`_


Frictionless
------------

The parameters to define a ``ConstraintFrictionless`` are the following:


* *field*, specified targeted field
* *fieldType*, specified targeted field type
* *constraint*, frictionless constraint

  * *format*
  * *type*
  * *required*
  * *unique*
  * *minLength*
  * *maxLength*
  * *minimum*
  * *maximum*
  * *pattern*
  * *enum*

* *value*, value expeted

Example:

.. code-block:: python

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
   CONSTRAINT_01 = dj.ConstraintFrictionless(title="Example frictionless constraint",
                                             name="example-const",
                                             resources=["example-resource"],
                                             field="field-to-validate",
                                             fieldType="string",
                                             constraint="maxLength",
                                             value=11,
                                             weight=5)

Frictionless schema
-------------------

The parameters to define a ``ConstraintFullFrictionless`` are the following:


* *schema*, a dictionary (or a frictionless ``Schema``), formatted as ``frictionless Schema``.

Example:

.. code-block:: python

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

   SCHEMA_01 = {
     "fields": [
       {"name":"col1", "type": "string"},
       {"name":"col2", "type": "integer"},
       {"name":"col3", "type": "float"},
     ]
   }

   # Example constraint. We will pass to a validator a full frictionless schema.
   CONSTRAINT_01 = dj.ConstraintFrictionless(title="Example frictionless_schema constraint",
                                             name="example-const",
                                             resources=["example-resource"],
                                             schema=SCHEMA_01,
                                             weight=5)

DuckDB
------

The parameters to define a ``ConstraintDuckDB`` are the following:


* *query*, an SQL query that will be executed on the resources

  * Please note that the query require some precautions

    * When you select from a resource, the resource must be written lowercase
    * The name of the resource where you select from must be in the list of resources passed to the constraint

* *expect*, expected tipology of result

  * *empty* (only for *check = rows*)
  * *non-empty* (only for *check = rows*)
  * *exact*
  * *range*
  * *minimum*
  * *maximum*

* *value*, value expected

  * Please note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows

    * "(num1, num2)" upper exclusive, lower exclusive
    * "(num1, num2]" upper exclusive, lower inclusive
    * "[num1, num2)" upper inclusive, lower exclusive
    * "[num1, num2]" upper inclusive, lower inclusive

  * *minimum* and *maximum* are inclusive

* *check*, tipology of result to evaluate

  * *rows* check number of rows
  * *value* check a single value, e.g. a *select count(\*)*. If a query result in more than one column, the evaluator will take into account only the first column in the first row

.. code-block:: python

   import datajudge as dj

   # Artifact Store
   STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                   type="local",
                                   uri="./djruns",
                                   isDefault=True)


   # Data Resource
   RES_LOCAL_01 = dj.DataResource(path="path-to-data",
                                  name="example_resource",
                                  store="local")


   # EXAMPLE CONSTRAINTS

   # Empty/non-empty table. The evaluation is allowed when check is "rows"

   # Expecting empty table as result of the validation query
   CONSTRAINT_01 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select * from example_resource",
                                       expect="empty",
                                       check="rows",
                                       weight=5)

   # Expecting non-empty table as result of the validation query
   CONSTRAINT_02 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select * from example_resource",
                                       expect="non-empty",
                                       check="rows",
                                       weight=5)

   # Exact value

   # Expecting a table with 10 rows
   CONSTRAINT_03 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select field from example_resource",
                                       expect="exact",
                                       check="rows",
                                       value=10,
                                       weight=5)

   # Expecting a table with 10 as result of the count
   CONSTRAINT_04 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select count(field) from example_resource",
                                       expect="exact",
                                       check="value",
                                       value=10,
                                       weight=5)

   # Minimum/maximum (both check are inclusive of the value)

   # Expecting a table with number of rows >= 10
   CONSTRAINT_05 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select field from example_resource",
                                       expect="minimum",
                                       check="rows",
                                       value=10,
                                       weight=5)

   # Expecting a table with result of count <= 10
   CONSTRAINT_06 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select count(field) from example_resource",
                                       expect="maximum",
                                       check="value",
                                       value=10,
                                       weight=5)

   # Range (value expect a string of parentheses and number)

   # Expecting a table with number of rows > 10 and <= 15
   CONSTRAINT_07 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select field from example_resource",
                                       expect="range",
                                       check="rows",
                                       value="(10,15]",
                                       weight=5)

   # Expecting a table with resulting value >= 10.87 and < 15.63
   CONSTRAINT_08 = dj.ConstraintDuckDB(title="Example duckdb constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select mean(field) from example_resource",
                                       expect="rows",
                                       check="value",
                                       value="[10.87,15.63)",
                                       weight=5)

SQLAlchemy
----------

The parameters to define a ``ConstraintSqlAlchemy`` are the following:


* *query*, an SQL query that will be executed on the database
* *expect*, expected tipology of result

  * *empty* (only for *check = rows*)
  * *non-empty* (only for *check = rows*)
  * *exact*
  * *range*
  * *minimum*
  * *maximum*

* *value*, value expected

  * Please note that when *expect* is equals to *range*, this parameter accepts a string formatted as follows

    * "(num1, num2)" upper exclusive, lower exclusive
    * "(num1, num2]" upper exclusive, lower inclusive
    * "[num1, num2)" upper inclusive, lower exclusive
    * "[num1, num2]" upper inclusive, lower inclusive

  * *minimum* and *maximum* are inclusive

* *check*, tipology of result to evaluate

  * *rows* check number of rows
  * *value* check a single value, e.g. a *select count(\*)*. If a query result in more than one column, the evaluator will take into account only the first column in the first row

.. code-block:: python

   import datajudge as dj

   # Artifact Store
   CONFIG_SQL_01 = {
       "connection_string": f"postgresql://user:password@host:port/database"
   }
   STORE_SQL_01 = dj.StoreConfig(name="postgres",
                                 type="sql",
                                 uri=f"sql://database",
                                 config=CONFIG_SQL_01)
   # Data Resource
   RES_SQL_01 = dj.DataResource(path=f"sql://schema.table",
                                name="example_resource",
                                store="postgres")

   # EXAMPLE CONSTRAINTS

   # The sqlalchemy constraints are basically the same as duckdb ones

   # Expecting empty table as result of the validation query
   CONSTRAINT_01 = dj.ConstraintDuckDB(title="Example sqlalchemy constraint",
                                       name="example-const",
                                       resources=["example_resource"],
                                       query="select * from example_resource",
                                       expect="empty",
                                       check="rows",
                                       weight=5)

Great Expectations
------------------

The parameters to define a ``ConstraintGreatExpectations`` are the following:

* *expectation*, expectation to apply on a resource
* *expectation_args*, arguments for the expectation

Note that for the moment the execution plugins require the presence of a user initialized ``Data context``.

.. code-block:: python

   import datajudge as dj

   # Artifact Store
   STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                   type="local",
                                   uri="./djruns",
                                   isDefault=True)

   # Data Resource
   RES_LOCAL_01 = dj.DataResource(path="path-to-data",
                                  name="example_resource",
                                  store="local")

   # EXAMPLE CONSTRAINTS

   # Expecting maximum column value to be between 10 and 50
   CONSTRAINT_01 = dj.ConstraintGreatExpectations(title="Example great expectations constraint",
                                                  name="example-const",
                                                  resources=["example_resource"],
                                                  expectation="expect_column_max_to_be_between",
                                                  expectation_args={"min_value": 10, "max_value": 50, "column": "target-column"},
                                                  weight=5)
