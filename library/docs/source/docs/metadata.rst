
Metadata
========

*Datajudge* can produce various metadata to describe both the various execution process and the input data. The metadata produced are:


* ``Run metadata``

  * Describe the run general execution, like execution time, libraries used, etc..

* ``Env metadata``

  * Describe the run enviroment execution, like system platform, hardware specification, etc..

* ``Datajudge Report``

  * A concise and anonymized version of the report created by a validation framework.

* ``Datajudge Schema``

  * A simple representation of the input data schema, describing columns names and types.

* ``Datajudge Profile``

  * A reduced and anonymized version of the report produced by a profiling framework.

* ``Artifact metadata``

  * A series of metadata that associate the artifacts persisted by the user with a run and indicate their location.


*Datajudge* logs this set of metadata into various backends. The library supports two types of backends:


* Local filesystem
* *DigitalHub* REST API (coming with this repository)
