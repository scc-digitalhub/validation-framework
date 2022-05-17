# Authentication

*Datajudge* allows passing credentials to backend storages through the `Client`.

- [Authentication](#authentication)
  - [Metadata store](#metadata-store)
  - [Artifact store](#artifact-store)
    - [Azure](#azure)
    - [S3](#s3)
    - [FTP](#ftp)
    - [HTTP](#http)
    - [SQL](#sql)
    - [ODBC](#odbc)

## Metadata store

The `Client` uses this store to log metadata to the backend.
At the moment there are two backends supported, the *local filesystem* and the *DigitalHub API backend*.

The *DigitalHub API backend* implements a basic authentication method. You can execute runs in the context of a specific `project`. You must provides to the `Client` three things:

- Project id
- URI of DigitalHub API
- Credentials dictionary with authentication type (basic with username/password, oauth with bearer token provided by user).

The way to build arguments for the `Client` is the following:

```python
import datajudge as dj

project_name = "projId"
API_URI = "http://ip_address:port"
```

For the authentication there are two options, *basic*

```python
API_CREDENTIALS = {
    "auth": "basic",
    "user": "username",
    "password": "password"
}
```

or *oauth* with a token provided by user.

```python
API_CREDENTIALS = {
    "auth": "oauth",
    "token": "token"
}
```

Setted the variables, the `Client` can be created.

```python

metadata_store = dj.StoreConfig(name="name", uri="uri", config=API_CREDENTIALS)
client = dj.Client(project_name=project_name,
                   metadata_store=metadata_store)
```

## Artifact store

The `Client` uses these objects to persist/fetch data into/from the backend storage.
*Datajudge* offers seven plugin out-of-the-box for the *Artifact stores*.

The mechanism of providing credentials to the store is the same as for the *Metadata store*:

```python
import datajudge as dj

CREDENTIALS = {"some": "config"}
STORE_TYPE = "store-type"
URI = "some-uri"

store = dj.StoreConfig(name="name", type=STORE_TYPE, uri=URI, config=CREDENTIALS)
client = dj.Client(store=store)
```

### Azure

**Store type**</br>
To initialize an Azure store use:

```python

STORE_TYPE = "azure"
```

**URI**</br>
URI must be a parsable `str` and must have *wasb* or *wasbs* scheme.

```python

URI = "wasbs://container(/partitions)"
```

**Credentials**</br>
The credentials must be provided inside a `dict`.
There are two ways of authentication, through *connection string* or through *access key* and *account name*.

- *connection string*

```python
CREDENTIALS = {
    "connection_string": "connection_string"
}
```

- *access key* and *account name*.

```python
CREDENTIALS = {
    "azure_access_key": "access_key",
    "azure_account_name": "account_name"
}
```

### S3

**Store type**</br>
To initialize an S3 store use:

```python

STORE_TYPE = "s3"
```

**URI**</br>
URI must be a parsable `str` and must have *s3* scheme.

```python

URI = "s3://container(/partitions)"
```

**Credentials**</br>
The credentials must be provided inside a `dict`.
The parameters are the `**kwargs` passed to a `boto3.client` constructor.

```python
CREDENTIALS = {
    "endpoint_url": "http://host:port/",
    "aws_access_key_id": "acc_key",
    "aws_secret_access_key": "sec_key"
}
```

### FTP

**Store type**</br>
To initialize an FTP store use:

```python

STORE_TYPE = "ftp"
```

**URI**</br>
URI must be a parsable `str` and must have *ftp* scheme.

```python

URI = "ftp://host:port/path"
```

**Credentials**</br>
The credentials can be provided in a `dict` or directly in the *endpoint path*. In any case, a valid *endpoint* must be provided.

- *endpoint*

```python

URI = "ftp://user:password@host:port/path"
```

- *dict*

```python
CREDENTIALS = {
    "host": "host",
    "port": "port",
    "user": "username",
    "password": "password"
}
```

### HTTP

**Store type**</br>
To initialize an HTTP store use:

```python

STORE_TYPE = "http"
```

**URI**</br>
URI must be a parsable `str` and must have *http* or *https* scheme.

```python

URI = "http://host:port/path"
```

**Credentials**</br>
The credentials must be provided inside a `dict`. We support *basic* and *bearer token* authentication.

```python
CREDENTIALS = {
    "auth": "basic",
    "user": "username",
    "password": "password"
}
```

or

```python
CREDENTIALS = {
    "auth": "oauth",
    "token": "token"
}
```

### SQL

**Store type**</br>
To initialize an SQL store use:

```python

STORE_TYPE = "sql"
```

**URI**</br>
URI must be a parsable `str` and must have *sql* scheme.

```python

URI = "sql://{db}.{schema}"
```

**Credentials**</br>
The credentials must be provided in a SQLAlchemy connection string.

```python

CREDENTIALS = {"connection_string": "dbtype+driver://user:pass@host:port/db"}
```

### ODBC

**Store type**</br>
To initialize an ODBC store use:

```python

STORE_TYPE = "odbc"
```

**URI**</br>
URI must be a parsable `str` and must have *odbc* or *dremio* scheme.

```python

URI = "odbc(/dremio)://{db_space}.{schema}"
```

**Credentials**</br>
The credentials must be provided in a `dict`.

```python

CREDENTIALS = {
    "host": "host",
    "port": "port",
    "user": "user",
    "password": "password",
    "driver": "ODBC-driver-name",
    "autocommit": True
}
```
