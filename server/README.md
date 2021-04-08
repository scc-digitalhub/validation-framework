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
* `auth.type` - Type of authentication to use. Only `basic` is currently supported, for which you will need to attach a `Authorization: Basic <Base64_encoded_username:password>` header to your API calls. To disable authentication, change it to `none` (or any other value).
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

Here is a list of notable endpoints. 6 kinds of documents may be saved: `artifact-metadata`, `data-profile`, `data-resource`, `run-metadata`, `short-report`, `short-schema`.

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
localhost:8200/api/project/<project_id>/data-resource?experiment_id=<experiment_id>&run_id=<run_id>&search=<search>
```
* `project_id` - Path variable, ID of the project.
* `experiment_id` - Optional parameter, ID of the experiment.
* `run_id` - Optional parameter, ID of the run.
* `search` - Optional parameter, a case-insensitive, diacritics-insensitive keyword to filter results by. Looks for a match in the `experiment_name` field of entries. For `artifact-metadata` documents only, the match may also be found in the `name` field instead.

---

### Create document
This API involves some significant differences depending on the kind of document to be created.

```
localhost:8200/api/project/<project_id>/data-resource
```
* `project_id` - Path variable, ID of the project.

The body for `data-profile`, `data-resource`, `run-metadata`, `short-report` and `short-schema` must include the following:
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

For any kind of document other than `artifact-metadata`, if a document already exists with the same `project_id`, `experiment_id` and `run_id`, it will result in an error.

For `run-metadata`, an optional parameter named `overwrite` may be specified.

If `overwrite` is specified and set to `true`, it will generate the document, and delete all previously existing documents of any kind that match the same combination of `project_id`, `experiment_id` and `run_id`.

If `overwrite` is not specified or set to a different value and a document with the same `project_id`, `experiment_id` and `run_id` already exists, it will result in an error.

The body for `artifact-metadata` must include the following:
* `experiment_id` - ID of the experiment.
* `run_id` - ID of the run.
* `name` - Name of the artifact.
* `uri` - Location of the artifact.

Optionally, the body may also include:
* `experiment_name` - Name of the experiment.

Example:
```
{
  "experiment_id":"experiment_validation",
  "run_id":"c51dbaf523e943c099b11a53a38e6a4f",
  "name": "file.sample",
  "uri":"a/b/c"
}
```

No error will occur for `artifact-metadata` if other documents contain the same combination of values.

---

### Update document
```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to update.

The content of the body follows the same structure as the endpoint for creation, but no fields are mandatory.

If `experiment_id` and `run_id` are specified, however, the back-end will (unless it's an `artifact-metadata` document) check that they indeed match the values of the document with the specified ID, and return an error if they don't.

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
