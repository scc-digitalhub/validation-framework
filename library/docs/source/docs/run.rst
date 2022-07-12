
Run
===

A ``Run`` is an orchestrator that executes data operations in a defined organizational context called ``experiment``.
The ``Run`` object is created by a ``Client`` and can perform various tasks:

* Log descriptive metadata
* Persist artifacts
* Fetch input data from the backend
* Manage validation/profiling/inference process

Run initialization
------------------

The ``Run`` wraps some methods exposed by other validation frameworks through the creation of plugins.
*Datajudge* can support different operational framework and libraries.
To create a ``Run``, we need to instantiate a ``Client``, define ``Stores`` and ``DataResources`` and provide a ``RunConfig``.

.. code-block:: python

   import datajudge as dj

   # Metadata Store (local)
   METADATA_STORE = dj.StoreConfig(title="Local Metadata Store",
                                   type="local",
                                   name="local_md",
                                   uri="./djruns")

   # Artifact store (local)
   STORE_LOCAL_01 = dj.StoreConfig(name="local",
                                   type="local",
                                   uri="./djruns",
                                   isDefault=True)

   RESOURCE = dj.DataResource(path="local/path/to/data",
                              name="res-name",
                              store="local")

   RUN_CFG = dj.RunConfig(
           inference=[{"library": "frictionless"}],
           validation=[{"library": "frictionless"}],
           profiling=[{"library": "frictionless"}]
   )


   client = dj.Client(metadata_store=METADATA_STORE,
                      store=STORE_LOCAL_01) # Could be also a list like [STORE_LOCAL_01]

The run can be initialized with the ``create_run`` method exposed by the ``Client`` API. The parameters required are:

* A single ``DataResource`` object or a list of them.
* A ``RunConfig`` object that contains the configuration for the framework used in the validation/profiling/inference processes.

The method ``create_run`` accepts also other three keywords arguments:

* ``experiment_name``, a name for the experiment the run belongs to
* ``run_id``, specify the ID of the run
* ``overwrite``, if there is already a run with the specified ID, enable the overwriting of all metadata tied to that run

.. code-block:: python


   run = client.create_run(resources=RESOURCE, run_config=RUN_CFG)


RunConfig
---------

The ``RunConfig`` is a *pydantic* object to that defines which operations the ``Run`` will perform. The ``RunConfig`` accepts three parameters:

* ``inference``
* ``validation``
* ``profiling``

Each one of these parameters configure which library will be used to perform the required operation. The library configuration is done like this:

.. code-block:: python

   inference_config = {
                   "library": "frictionless",
                   "execArgs": {},
                   "tmpFormat": "csv"
   }

   RUN_CFG = dj.RunConfig(
           inference=[inference_config]
   )

In this example we configure an *inference* operation using a ``dict``. The arguments are the following:


* ``library``, mandatory, defines the framework used in the operation
* ``execArgs``, optional, arguments passed to the operation performed by the framework
* ``tmpFormat``, optional, format used to store/fetch artifacts from ``ArtifactStore``

Run execution
-------------

You can now use the ``Run`` as context manager ...

.. code-block:: python


   with run:
       # SOME CODE
       run.some_method()

... or as a generic object.


.. code-block:: python


   run.some_method()

Note that if the ``Run`` is used outside the context manager, some metadata will not be produced, i.e. run duration.
The ``Run`` exposes a variety of methods. In general, these methods cover four needs:


* Execute a specific operation over some resources

  * `Validation <validation.html>`_
  * `Profiling <profiling.html>`_
  * `Inference <inference.html>`_

* Log datajudge metadata to a backend
* Persist artifact produced by the execution frameworks
* Persist input data as artifacts

An example can be as follows:

.. code-block:: python


   with run:

       # Method that executes inference over run's resources
       run.infer()

       # Log the datajudge version of an inferred schema
       run.log_schema()

       # Persist the artifact produced by the inference framework
       run.persist_schema()

       # Persist the input data as artifact
       run.persist_data()
