# Authentication

*Datajudge* allows passing credential to backend storage through the `Client`.
When a `Client` is instantiated, you can set the credentials for three `store` objects:

- `Metadata store`
- `Artifact store`
- `Data store`

## Metadata store

The `Client` uses this store to log metadata to the backend.
At the moment there are two backends supported, the *local filesystem* and the *DigitalHub API backend*.

The *DigitalHub API backend* implements a basic authentication method. You can execute runs in the context of a specific `project`. You must provides to the `Client` three things:

- Project id
- Endpoint of DigitalHub API
- Credentials dictionary with authentication type, username and a password.

The way to build arguments for the `Client` is the following:

```python
import datajudge as dj

PROJECT_ID = "projId"
API_ENDPOINT = "http://ip_address:port"
API_CREDENTIALS = {
    "auth": "basic",
    "user": "username",
    "password": "password"
}

client = dj.Client(project_id=PROJECT_ID,
                   metadata_store_uri=API_ENDPOINT,
                   metadata_store_config=API_CREDENTIALS)

```

## Artifact/Data store

The `Client` uses these objects to persist/fetch data into/from the backend storage.
*Datajudge* offers five plugin out-of-the-box for *Artifact/Data store*, and four of them may require authentication:

- Azure
- S3
- FTP
- HTTP

Similarly to the *Metadata store*, the way of passing credentials to the `Client` is the following:

```python
import datajudge as dj

client = dj.Client(artifact_store_uri=ENDPOINT,
                   artifact_store_config=CREDENTIALS,
                   data_store_uri=ENDPOINT,
                   data_store_config=CREDENTIALS)

```

### Azure

**Endpoint**</br>
The endpoint is a parsable URI `str` and must have *wasb* or *wasbs* scheme.

```python

ENDPOINT = "wasbs://container/partition(s)"
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

**Endpoint**</br>
The endpoint is a parsable URI `str` and must have *s3* scheme.

```python

ENDPOINT = "s3://container/partition(s)"
```

**Credentials**</br>
The credentials must be provided inside a `dict`.
The parameters are the `**kwargs` passed to a `boto3.client` constructor.

```python
CREDENTIALS = {
    "endpoint_url": "http://host:port/",
    "aws_access_key_id": "acc_key",
    "aws_secret_access_key": "sec_key",
    "region_name": 'us-east-1'
}
```

### FTP

**Endpoint**</br>
The endpoint is a parsable URI `str` and must have *ftp* scheme.

```python

ENDPOINT = "ftp://host:port/path"
```

**Credentials**</br>
The credentials can be provided in a `dict` or directly in the *endpoint path*.

- *endpoint*

```python

ENDPOINT = "ftp://user:password@host:port/path"
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

**Endpoint**</br>
The endpoint is a parsable URI `str` and must have *http* or *https* scheme.

```python

ENDPOINT = "http://host:port/path"
```

**Credentials**</br>
The credentials must be provided inside a `dict`

```python
CREDENTIALS = {
    "auth": "basic",
    "user": "username",
    "password": "password"
}
```
