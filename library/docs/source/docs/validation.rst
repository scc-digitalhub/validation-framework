
Validation
==========

The validation is the process where a framework validate one or more ``DataResource`` in accordance to a given ``Constraint``.


Run methods
-----------

.. code-block:: python

   import datajudge as dj

   # Creating run ...

   with run:

       run.validate()
       run.validate_wrapper()
       run.validate_datajudge()
       run.log_report()
       run.persist_report()

Execution methods
^^^^^^^^^^^^^^^^^

Execution method tell plugings to execute validation over a resource. All this methods accept specific framework arguments as argument and a list of ``Constraint`` to validate.

* ``run.validate()``, execute both framework validation and datajudge report parsing
* ``run.validate_wrapper()``, execute only framework validation, return a specific framework artifact
* ``run.validate_datajudge()``, execute both framework validation and datajudge report parsing, return a ``DatajudgeReport``

Data and metadata persistence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``run.log_report()``, log ``DatajudgeReport`` into the ``MetadataStore``
* ``run.validate()``, persist artifact into the default ``ArtifactStore``


Supported libraries
-------------------

* `Frictionless`_
* `DuckDB`_
* `SQLAlchemy`_
* `Great Expectations`_


Frictionless
^^^^^^^^^^^^

.. code-block:: python

   run_config = {

       # The only parameter accepted is "frictionless"
       "library": "frictionless",

       # execArgs accepted are the ones passed to the method validate()
       "execArgs": {}
   }


DuckDB
^^^^^^

.. code-block:: python

   run_config = {

       # The only parameter accepted is "duckdb"
       "library": "duckdb",

       # There are no suitable execution arguments for the duckdb validator
       "execArgs": {}

   }


SQLAlchemy
^^^^^^^^^^

The ``sqlalchemy`` validator executes query defined in a *constraints* on the database side. To execute a validation without execution errors, there MUST be at least one user defined ``SQLArtifactStore`` passed to a ``Client`` and a ``DataResource`` associated with that store.

.. code-block:: python

   run_config = {
       # The only parameter accepted is "sqlalchemy"
       "library": "sqlalchemy",

       # There are no suitable execution arguments for the duckdb validator
       "execArgs": {}
   }


Great Expectations
^^^^^^^^^^^^^^^^^^

The ``great_expectations`` validator executes an expectation specified in a *constraint* on a ``DataResource``.

.. code-block:: python

   run_config = {
       "library": "great_expectations",

       # There are no suitable execution arguments for the great_expectations validator
       "execArgs": {}

   }
