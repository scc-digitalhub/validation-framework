# Back-end to store validation-related documents

## Requirements

The back-end needs access to a *MongoDB* database to store documents into. Make sure you have an instance available, either locally or remotely.

## Configuration

The `server/src/main/resources/application.yml` file contains a list of settings for the back-end. Each setting is presented in the form:
```
${NAME_OF_ENVIRONMENT_VARIABLE:default_value}
```

A brief description of each currently available setting is as follows:

* `server.port` - Port to host the service on.
* `server.error.include-message` - When to include self-explaining messages when an API results in an error.
* `spring.data.mongodb.uri` - Connection URI to the MongoDB server.


## Installing and running

To install and run the back-end, change directory to the `server` sub-folder:
```
cd server
```

Compile with Maven:
```
mvn clean install
```

Run:
```
mvn exec:java -Dexec.mainClass="it.smartcommunitylab.validationstorage.ValidationStorageApplication"
```

A list of available endpoints and their use should now be hosted at http://localhost:8200/swagger-ui.html.

## Endpoints

Here is a list of notable endpoints. 4 kinds of documents may be saved: `artifact-metadata`, `data-resource`, `run-metadata`, `short-report`.

The endpoints for each kind are identical, so only those related to `data-resource` are reported in this section. Simply replace `data-resource` with whichever other kind of document you need.

---

### Get document by ID:

```
localhost:8200/api/data-resource/<document_id>
```
* `document_id` - Path variable, ID of the document you wish to retrieve.

---

### Get documents by project ID
```
localhost:8200/api/project/<project_id>/data-resource?experiment_name=<exp_name>&run_id=<run_id>
```
* `project_id` - Path variable, ID of the project.
* `exp_name` - Optional parameter, name of the experiment.
* `run_id` - Optional parameter, ID of the run.

---

### Create document
```
localhost:8200/api/data-resource?projectId=<project_id>
```
* `project_id` - Mandatory parameter, ID of the project.

The body for `data-resource`, `run-metadata` and `short-report` must include the following:
* `experiment_name` - Name of the experiment.
* `run_id` - ID of the run.
* `contents` - Any object, can contain any valid JSON.

Example:
```
{
  "experiment_name": "exp1",
  "run_id": "run1",
  "contents": {
    "a":"aaa",
    "b":"bbb"
  }
}
```

However, the body for `artifact-metadata` must include the following:
* `experiment_name` - Name of the experiment.
* `run_id` - ID of the run.
* `name` - Name of the artifact.
* `uri` - Location of the artifact.

Example:
```
{
  "id":"60477dbfc30c0d5703a7da5c",
  "experiment_name":"experiment_validation",
  "run_id":"c51dbaf523e943c099b11a53a38e6a4f",
  "name": "file.sample",
  "uri":"a/b/c"
}
```

---

### Update document
```
localhost:8200/api/data-resource/<document_id>
```
* `document_id` - Path variable, ID of the document you wish to update.

The content of the body follows the same structure as the endpoint for creation.

The `experiment_name` and `run_id` fields are not mandatory for `data-resource`, `run-metadata` and `short-report`, but, if specified, the back-end will check they match the ID.

---

### Delete document by ID
```
localhost:8200/api/data-resource/<document_id>
```
* `document_id` - Path variable, ID of the document you wish to retrieve.

---

### Delete documents by project ID
```
localhost:8200/api/project/<project_id>/data-resource?experiment_name=<exp_name>&run_id=<run_id>
```
* `project_id` - Path variable, ID of the project.
* `exp_name` - Optional parameter, name of the experiment.
* `run_id` - Optional parameter, ID of the run.
