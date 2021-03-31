# Back-end to store validation-related documents

## Requirements

The back-end needs access to a *MongoDB* database to store documents into. Make sure you have an instance available, either locally or remotely.

## Configuration

The `server/src/main/resources/application.yml` file contains a list of settings for the back-end. Each setting is presented in the form:
```
${NAME_OF_ENVIRONMENT_VARIABLE:default_value}
```

The main settings are:

* `server.port` - Port to host the service on.
* `server.error.include-message` - When to include self-explaining messages when an API results in an error.
* `spring.data.mongodb.uri` - Connection URI to the MongoDB server.

### Authentication

The `application.yml` file also contains a number of settings for authentication:
* `auth.type` - Type of authentication to use. Only `basic` is currently supported. To disable authentication, change it to `none` (or any other value).
* `auth.project-authority-prefix` - A prefix used to identify authorities over projects.
* `auth.users` - A list of users, identified by `username` and `password`. The `authorities` element lists projects the user is allowed to work on. Each project must be presented as a string made by the same value as `auth.project-authority-prefix` followed by the project ID.

For example:
```
auth:
  type: basic
  project-authority-prefix: PROJECT_
  users:
    - username: admin
      password: password
      authorities: PROJECT_proj1, PROJECT_proj2
    - username: other
      password: password
      authorities: PROJECT_proj1, PROJECT_proj3
```

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

The endpoints for each kind are identical (with some exceptions described in the corresponding subsections), so only those related to `data-resource` are reported in this section. Simply replace `data-resource` with whichever other kind of document you need.

---

### Get document by ID:

```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to retrieve.

---

### Get documents by project ID
```
localhost:8200/api/project/<project_id>/data-resource?experiment_id=<experiment_id>&run_id=<run_id>
```
* `project_id` - Path variable, ID of the project.
* `experiment_id` - Optional parameter, ID of the experiment.
* `run_id` - Optional parameter, ID of the run.

---

### Create document
This API involves some significant differences depending on the kind of document to be created.

```
localhost:8200/api/project/<project_id>/data-resource
```
* `project_id` - Path variable, ID of the project.

The body for `data-resource`, `run-metadata` and `short-report` must include the following:
* `experiment_id` - ID of the experiment.
* `run_id` - ID of the run.

Optionally, the body may also include:
* `experiment_name` - Name of the experiment.
* `contents` - Any object, can contain any valid JSON.

Example:
```
{
  "experiment_id": "exp1",
  "experiment_name": "some_experiment",
  "run_id": "run1",
  "contents": {
    "a":"aaa",
    "b":"bbb"
  }
}
```

For `data-resource` and `short-report`, if a document already exists with the same `project_id`, `experiment_id` and `run_id`, it will result in an error.

For `run-metadata`, an optional parameter named `overwrite` may be specified.

If `overwrite` is specified and set to `true`, it will generate the document, and delete all previously existing documents of any kind that match the same combination of `project_id`, `experiment_id` and `run_id`.

If `overwrite` is not specified or set to a different value, it will behave the same as `data-resource` and `short-report`, resulting in an error if a document with the same `project_id`, `experiment_id` and `run_id` already exists.

The body for `artifact-metadata` must include the following:
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

No error will occur for `artifact-metadata` if other documents contain the same values in these fields.

---

### Update document
```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to update.

The content of the body follows the same structure as the endpoint for creation.

The `experiment_id` and `run_id` fields are not mandatory for `data-resource`, `run-metadata` and `short-report`, but, if specified, the back-end will check if they indeed match the values of the document with the specified ID. If they do not, it will result in an error.

---

### Delete document by ID
```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to retrieve.

---

### Delete documents by project ID
```
localhost:8200/api/project/<project_id>/data-resource?experiment_id=<experiment_id>&run_id=<run_id>
```
* `project_id` - Path variable, ID of the project.
* `experiment_id` - Optional parameter, ID of the experiment.
* `run_id` - Optional parameter, ID of the run.
