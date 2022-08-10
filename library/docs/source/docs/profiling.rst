
Profiling
=========

The profiling is the process where a framework try to profile a ``DataResource``.

Supported libraries
-------------------

* `Frictionless`_
* `Pandas Profiling`_
* `Great Expectation`_


Run methods
-----------

.. code-block:: python

   import datajudge as dj

   # Creating run ...

   with run:

       run.profile()
       run.profile_wrapper()
       run.profile_datajudge()
       run.log_profile()
       run.persist_profile()

Execution methods
^^^^^^^^^^^^^^^^^

Execution method tell plugings to execute profiling over a resource. All this methods accept specific framework arguments as argument.

* ``run.profile()``, execute both framework profiling and datajudge profile parsing
* ``run.profile_wrapper()``, execute only framework profiling, return a specific framework artifact
* ``run.profile_datajudge()``, execute both framework profiling and datajudge profile parsing, return a ``DatajudgeProfile``

Data and metadata persistence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``run.log_profile()``, log ``DatajudgeProfile`` into the ``MetadataStore``
* ``run.profile()``, persist artifact into the default ``ArtifactStore``


Frictionless
------------

.. code-block:: python

   run_config = {

       # The only parameter accepted is "frictionless"
       "library": "frictionless",

       # execArgs accepted are the ones passed to the constructor of Resource().
       "execArgs": {}

   }


Pandas Profiling
----------------

.. code-block:: python

   run_config = {

       # The only parameter accepted is "pandas_profiling"
       "library": "pandas_profiling",

       # execArgs accepted are the ones passed to the method ProfileReport(). E.g.:
       "execArgs": {"minimal": True}

   }


Great Expectation
-----------------

The ``great_expectations`` validator executes an expectation specified in a *constraint* on a ``DataResource``.

.. code-block:: python

   run_config = {
       "library": "great_expectations",

       # There are no suitable execution arguments for the great_expectations validator
       "execArgs": {}

   }
