
Inference
=========

The inference is the process where a framework try to infer the data schema of a ``DataResource``.

Run methods
-----------

.. code-block:: python

   import datajudge as dj

   # Creating run ...

   with run:

       run.infer()
       run.infer_wrapper()
       run.infer_datajudge()
       run.log_schema()
       run.persist_schema()

Execution methods
^^^^^^^^^^^^^^^^^

Execution method tell plugings to execute inference over a resource. All this methods accept specific framework arguments as argument.


* ``run.infer()``, execute both framework inference and datajudge schema parsing
* ``run.infer_wrapper()``, execute only framework inference, return a specific framework artifact
* ``run.infer_datajudge()``, execute both framework inference and datajudge schema parsing, return a ``DatajudgeSchema``

Data and metadata persistence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* ``run.log_schema()``, log ``DatajudgeSchema`` into the ``MetadataStore``
* ``run.infer()``, persist artifact into the default ``ArtifactStore``


Supported libraries
-------------------

* `Frictionless`_


Frictionless
^^^^^^^^^^^^

.. code-block:: python

   run_config = {

       # The only parameter accepted is "frictionless"
       "library": "frictionless",

       # execArgs accepted are the ones passed to the method Schema.describe().
       # Note that arguments `path` and `name` are already taken.
       "execArgs": {}

   }
