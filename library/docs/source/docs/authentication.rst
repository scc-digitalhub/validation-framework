
Authentication
==============

*Datajudge* allows passing credentials to backend storages through the ``Client``.


* `Metadata store`_
* `Artifact store`_

  * `Azure`_
  * `S3`_
  * `FTP`_
  * `HTTP`_
  * `SQL`_
  * `ODBC`_


Metadata store
--------------

The ``Client`` uses this store to log metadata to the backend.
At the moment there are two backends supported, the *local filesystem* and the *DigitalHub API backend*.

The *DigitalHub API backend* implements a basic authentication method. You can execute runs in the context of a specific ``project``. You must provides to the ``Client`` three things:


* Project id
* URI of DigitalHub API
* Credentials dictionary with authentication type (basic with username/password, oauth with bearer token provided by user).

The way to build arguments for the ``Client`` is the following:

.. code-block:: python

   import datajudge as dj

   project_name = "projId"
   API_URI = "http://ip_address:port"

For the authentication there are two options, *basic*

.. code-block:: python

   API_CREDENTIALS = {
       "auth": "basic",
       "user": "username",
       "password": "password"
   }

or *oauth* with a token provided by user.

.. code-block:: python

   API_CREDENTIALS = {
       "auth": "oauth",
       "token": "token"
   }

Setted the variables, the ``Client`` can be created.

.. code-block:: python


   metadata_store = dj.StoreConfig(name="name", uri="uri", config=API_CREDENTIALS)
   client = dj.Client(project_name=project_name,
                      metadata_store=metadata_store)



Artifact store
--------------

The ``Client`` uses these objects to persist/fetch data into/from the backend storage.
*Datajudge* offers seven plugin out-of-the-box for the *Artifact stores*.

The mechanism of providing credentials to the store is the same as for the *Metadata store*:

.. code-block:: python

   import datajudge as dj

   CREDENTIALS = {"some": "config"}
   STORE_TYPE = "store-type"
   URI = "some-uri"

   store = dj.StoreConfig(name="name", type=STORE_TYPE, uri=URI, config=CREDENTIALS)
   client = dj.Client(store=store)

Azure
^^^^^

| **Store type**
|
| To initialize an Azure store use:

.. code-block:: python


   STORE_TYPE = "azure"

| **URI**
|
| URI must be a parsable ``str`` and must have *wasb* or *wasbs* scheme.

.. code-block:: python


   URI = "wasbs://container(/partitions)"

| **Credentials**
|
| The credentials must be provided inside a ``dict``. There are two ways of authentication, through *connection string* or through *access key* and *account name*.


* *connection string*

.. code-block:: python

   CREDENTIALS = {
       "connection_string": "connection_string"
   }


* *access key* and *account name*.

.. code-block:: python

   CREDENTIALS = {
       "azure_access_key": "access_key",
       "azure_account_name": "account_name"
   }

S3
^^

| **Store type**
|
| To initialize an S3 store use:

.. code-block:: python


   STORE_TYPE = "s3"

| **URI**
|
| URI must be a parsable ``str`` and must have *s3* scheme.

.. code-block:: python


   URI = "s3://container(/partitions)"

| **Credentials**
|
| The credentials must be provided inside a ``dict``. The parameters are the ``**kwargs`` passed to a ``boto3.client`` constructor.

.. code-block:: python

   CREDENTIALS = {
       "endpoint_url": "http://host:port/",
       "aws_access_key_id": "acc_key",
       "aws_secret_access_key": "sec_key"
   }

FTP
^^^

| **Store type**
|
| To initialize an FTP store use:

.. code-block:: python


   STORE_TYPE = "ftp"

| **URI**
|
| URI must be a parsable ``str`` and must have *ftp* scheme.

.. code-block:: python


   URI = "ftp://host:port/path"

| **Credentials**
|
| The credentials can be provided in a ``dict`` or directly in the *endpoint path*. In any case, a valid *endpoint* must be provided.


* *endpoint*

.. code-block:: python


   URI = "ftp://user:password@host:port/path"


* *dict*

.. code-block:: python

   CREDENTIALS = {
       "host": "host",
       "port": "port",
       "user": "username",
       "password": "password"
   }

HTTP
^^^^

| **Store type**
|
| To initialize an HTTP store use:

.. code-block:: python


   STORE_TYPE = "http"

| **URI**
|
| URI must be a parsable ``str`` and must have *http* or *https* scheme.

.. code-block:: python


   URI = "http://host:port/path"

| **Credentials**
|
| The credentials must be provided inside a ``dict``. We support *basic* and *bearer token* authentication.

.. code-block:: python

   CREDENTIALS = {
       "auth": "basic",
       "user": "username",
       "password": "password"
   }

or

.. code-block:: python

   CREDENTIALS = {
       "auth": "oauth",
       "token": "token"
   }

SQL
^^^

| **Store type**
|
| To initialize an SQL store use:

.. code-block:: python


   STORE_TYPE = "sql"

| **URI**
|
| URI must be a parsable ``str`` and must have *sql* scheme.

.. code-block:: python


   URI = "sql://{db}.{schema}"

| **Credentials**
|
| The credentials must be provided in a SQLAlchemy connection string.

.. code-block:: python


   CREDENTIALS = {"connection_string": "dbtype+driver://user:pass@host:port/db"}

ODBC
^^^^

| **Store type**
|
| To initialize an ODBC store use:

.. code-block:: python


   STORE_TYPE = "odbc"

| **URI**
|
| URI must be a parsable ``str`` and must have *odbc* or *dremio* scheme.

.. code-block:: python


   URI = "odbc(/dremio)://{db_space}.{schema}"

| **Credentials**
|
| The credentials must be provided in a ``dict``.

.. code-block:: python


   CREDENTIALS = {
       "host": "host",
       "port": "port",
       "user": "user",
       "password": "password",
       "driver": "ODBC-driver-name",
       "autocommit": True
   }
