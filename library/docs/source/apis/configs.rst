Configurations
==============

* `Stores`_
* `Data Resource`_
* `Run configuration`_
* `Constraints`_

Stores
------

datajudge.StoreConfig
^^^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: datajudge.utils.config::StoreConfig

Data Resource
-------------

datajudge.DataResource
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: datajudge.data.data_resource::DataResource

Run configuration
-----------------

datajudge.RunConfig
^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: datajudge.utils.config::ExecConfig

.. autopydantic_model:: datajudge.utils.config::RunConfig

Constraints
-----------

Every constraint inherit from the base Contraint model.

datajudge.Constraint
^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: datajudge.utils.config::Constraint

datajudge.ConstraintFrictionless
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: datajudge.utils.config::ConstraintFrictionless

datajudge.ConstraintFullFrictionless
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: datajudge.utils.config::ConstraintFullFrictionless


datajudge.ConstraintDuckDB
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: datajudge.utils.config::ConstraintDuckDB

datajudge.ConstraintSqlAlchemy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: datajudge.utils.config::ConstraintSqlAlchemy

datajudge.ConstraintGreatExpectation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autopydantic_model:: datajudge.utils.config::ConstraintGreatExpectation


