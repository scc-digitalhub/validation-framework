# Back-end to store validation-related documents

## Requirements

The back-end needs access to a *MongoDB* database to store documents into. Make sure you have an instance available, either locally or remotely.

## Configuration

Two files are used for configuration: `server/src/main/resources/application.yml` and `server/src/main/resources/application-local.yml`.

`application.yml` sets the default values, while `application-local.yml` is a file you must provide, with the appropriate configuration. You can duplicate and rename `application-local.yml.template`, found in that same folder, to  `application-local.yml` and start editing values from that.

Some settings in `application.yml` are presented as follows, to take a value from an environment variable if present, or otherwise use a default:
```
${NAME_OF_ENVIRONMENT_VARIABLE:default_value}
```

You can ignore `application.yml` and only edit `application-local.yml`.

---

Notable settings you likely need to change are:
* `spring.data.mongodb.uri` - Connection URI to the MongoDB server.
* `auth.enabled` - Either `true` or `false`. *Basic* and *OAuth2* are supported. When enabled, you will need to attach a `Authorization` header to your API calls, with value `Basic <Base64_encoded_username:password>` for *Basic*, or `Bearer <token>` for *OAuth2*.

---

These are only meaningful if authentication is enabled:
* `spring.security.oauth2.client.registration.aac.client-id` - For **OAuth2** auth. Client ID of this application in AAC.
* `spring.security.oauth2.client.registration.aac.client-secret` - For **OAuth2** auth. Client secret of this application in AAC.
* `spring.security.oauth2.client.provider.aac.issuer-uri` - For **OAuth2** auth. Address of JWT issuer.
* `spring.security.oauth2.client.provider.aac.jwk-set-uri` - For **OAuth2** auth. Full path to end-point for setting JWK.
* `spring.security.oauth2.client.provider.aac.user-name-attribute` - For **OAuth2** auth. AAC attribute to use for the user name (you probably don't need to change this).

* `spring.security.oauth2.resourceserver.jwt.issuer-uri` - For **OAuth2** auth. Address of JWT issuer (same value as `...client.provider.aac.issuer-uri`).
* `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` - For **OAuth2** auth. Full path to end-point for setting JWK (same value as `...client.provider.aac.jwk-set-uri`).
* `spring.security.oauth2.resourceserver.client-id` - For **OAuth2** auth. Client ID of this application in AAC (same value as `...registration.aac.client-id`).

* `auth.users` - For **Basic** auth. A list of users, identified by `username` and `password`. The `authorities` element lists projects the user is allowed to work on. Each project is presented as a string made by the same value as `auth.project-authority-prefix` followed by the project ID.

For example:
```
auth:
  enabled: true
  users:
    - username: admin
      password: password
      authorities: PROJECT_proj1, PROJECT_proj2
    - username: other
      password: password
      authorities: PROJECT_proj1, PROJECT_proj3
```

---

Other settings (which you can probably ignore) are described here. Some of them are in `application.yml`.
* `server.port` - Port to host the service on.
* `server.error.include-message` - When to include self-explaining messages when an API results in an error.
* `auth.project-authority-prefix` - For when auth is enabled. A prefix used to identify authority over a project.
* `auth.aac-claim` - For **OAuth2** auth. The name of the claim in AAC which describes the user's authorities.
* `auth.aac-claim-projects` - For **OAuth2** auth. The name of the list which contains the projects the user has authority over.


## Enabling the UI
To enable the UI, it has to be configured and built. Then, the resulting files must be moved to the appropriate path.

Change directory to the `ui` sub-folder, then run the following to install the necessary modules (may take several minutes):
```
npm install
```

Duplicate the `.env.template` file and rename the new one to simply `.env`. Inside is the configuration of the UI:
* `REACT_APP_BACKEND_ADDRESS`: The address of the backend. Make sure the port corresponds to the same as the value indicated in `application.yml` under `server.port`.

Next, run the following command. It will create a new folder named `build`.
```
npm run-script build
```

Move the `build` folder you just obtained to the server, under `validation-framework\server\src\main\resources`. Once it's there, rename `build` to `public`.

When the server is run, the UI will be available at `localhost:8200`.

## Installing and running

To install and run the back-end, change directory to the `server` sub-folder, then compile with Maven (the extra parameter loads the `application-local.yml` file):
```
mvn clean install -Dspring.profiles.active=local
```

Run:
```
mvn spring-boot:run -Dspring-boot.run.profiles=local
```

A list of available endpoints and their use should now be hosted at http://localhost:8200/swagger-ui.html.

## Endpoints

Several kinds of documents are handled and each of them has end-points for creating, reading, updating and deleting: `artifact-metadata`, `data-profile`, `data-resource`, `experiment`, `project`, `run-environment`, `run-metadata`, `short-report`, `short-schema`.

`project` end-points have the most different behavior, so a dedicated section is presented first.

For other types of documents, end-points and their behavior are almost identical regardless of the type, so only those related to `data-resource` are reported in this section. Simply replace `data-resource` in the path with whichever other kind of document you need.

Keep in mind that an error will be returned if authentication is enabled and the user is trying to act on a project (or a document belonging to a project) they have no authority over.

---

### Project

#### Create a project (POST):
```
localhost:8200/api/project
```
Contents of the body:
* `id` -**Mandatory**, ID of the project.
* `name` - *Optional*, name of the project.

Example:
```
{
  "id": "proj1",
  "name": "Project 1"
}
```

---

#### Get all projects (GET):
```
localhost:8200/api/project
```
Lists all projects, but if authentication is enabled, only those the authenticated user is authorized to see are present.

---

#### Get project by ID (GET):
```
localhost:8200/api/project/<project_id>
```
* `project_id` - Path variable, ID of the project.

---

#### Update a project (PUT):
```
localhost:8200/api/project/<project_id>
```
* `project_id` - Path variable, ID of the project.

Contents of the body:
* `id` -*Optional*, ID of the project. This value can't actually be updated. If specified, the back-end will check that it matches the `project_id` specified as path variable. Consider this an extra measure to ensure you're updating the correct document.
* `name` - *Optional*, updated name of the project.

Example:
```
{
  "id": "proj1",
  "name": "Proj 1"
}
```

---

#### Delete a project:
```
localhost:8200/api/project/<project_id>
```
* `project_id` - Path variable, ID of the project.
Note that **all documents of other types under this project will also be deleted**.

---

### Other documents

As mentioned before, for all other types of documents, end-points and their behaviors are almost identical regardless of type.

Some differences may be present, in which case they will be described, but otherwise only end-points related to `data-resource` are detailed in this section. Simply replace `data-resource` in the path with whichever other kind of document you need.

### Create document (POST)
This end-point involves the most significant differences depending on the kind of document, so it contains a number of sub-sections to ease explanation.

#### experiment
You do not actually need to create `experiment` documents. When documents of types under `experiment` (`artifact-metadata`, `data-profile`, `data-resource`, `run-environment`, `run-metadata`, `short-report`, `short-schema` ) are created, the back-end will automatically create the `experiment` with the information it receives.

For completeness, there is still an end-point for this, which you can use as follows if you'd like.

```
localhost:8200/api/project/<project_id/experiment
```
* `project_id` - Path variable, ID of the project.

Contents of the body:
* `experiment_id` -**Mandatory**, ID of the experiment. Note it is only unique within the project it belongs to.
* `experiment_name` - *Optional*, name of the experiment.

Example:
```
{
  "experiment_id": "exp1",
  "experiment_name": "Exp 1"
}
```

#### run-metadata
```
localhost:8200/api/project/<project_id>/run-metadata?overwrite=<true_or_false>
```
* `project_id` - Path variable, ID of the project.
* `overwrite` - *Optional* parameter, ID of the project.

Contents of the body:
* `experiment_id` - **Mandatory**, ID of the experiment.
* `run_id` - **Mandatory** ID of the run. Note it is only unique within the project and experiment it belongs to.
* `experiment_name` - *Optional*, name of the experiment.
* `contents` - *Optional*, any object, can contain any valid JSON.

Example:
```
{
  "experiment_id": "exp1",
	"experiment_name": "Exp 1",
	"run_id": "run1",
	"contents": {
		"a":"aaa",
		"b":"bbb"
	}
}
```

This document represents a run, which is why it presents a `overwrite` parameter.

If `overwrite` is specified and set to `true`, it will generate the document and delete (if found) the previous `run-metadata` document that matches the same combination of `project_id`, `experiment_id` and `run_id`.

All documents of other types that match this combination will also be deleted. As you'd expect, `project` and `experiment` documents will be unaffected, as they reside above `run-metadata`.

If `overwrite` is not specified, or set to `false`, and a document with the same `project_id`, `experiment_id` and `run_id` already exists, it will just result in an error.

#### artifact-metadata
```
localhost:8200/api/project/<project_id>/artifact-metadata
```
* `project_id` - Path variable, ID of the project.

Contents of the body:
* `experiment_id` - **Mandatory**, ID of the experiment.
* `run_id` - **Mandatory**, ID of the run.
* `name` - **Mandatory**, name of the file.
* `uri` - **Mandatory**, location of the file.
* `experiment_name` - *Optional*, name of the experiment.

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

#### data-profile, data-resource, run-environment, short-report, short-schema
```
localhost:8200/api/project/<project_id>/<document_type>
```
* `project_id` - Path variable, ID of the project.
* `document_type` - Path variable, `data-profile`, `data-resource`, `run-environment`, `short-report` or `short-schema`. These documents behave identically.

Contents of the body:
* `experiment_id` - **Mandatory**, ID of the experiment.
* `run_id` - **Mandatory**, ID of the run.
* `experiment_name` - *Optional*, name of the experiment.
* `contents` - *Optional*, any object, can contain any valid JSON.

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

If a document already exists with the same `project_id`, `experiment_id` and `run_id`, it will result in an error.

---

### Get document by ID (GET):

```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to retrieve.

---

### Get documents by project ID (GET)
```
localhost:8200/api/project/<project_id>/data-resource?experiment_id=<experiment_id>&run_id=<run_id>&search=<search>
```
* `project_id` - Path variable, ID of the project.
* `experiment_id` - *Optional* parameter, ID of the experiment.
* `run_id` - *Optional* parameter, ID of the run. Unused for documents of type `experiment`.
* `search` - *Optional* parameter, a case-insensitive, diacritics-insensitive keyword to filter results by. Looks for a match in the `experiment_name` field of entries. For `artifact-metadata` documents only, the match may also be found in the `name` field instead.

---

### Update document (PUT)
```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to update.

The content of the body follows the same structure as the endpoint for creation, but no fields are mandatory.

For any document except `artifact-metadata`: `experiment_id` and `run_id` cannot be changed, but if specified, the back-end will check that they indeed match the values of the document with the specified ID, and return an error if they don't.

---

### Delete document by ID (DELETE)
```
localhost:8200/api/project/<project_id>/data-resource/<document_id>
```
* `project_id` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `document_id` - Path variable, ID of the document you wish to delete.

Keep in mind that if an `experiment` document is deleted, all related documents of types under it will also be deleted. As you'd expect, `project` documents will be unaffected, as they reside above `experiment`.

---

### Delete documents by project ID (DELETE)
```
localhost:8200/api/project/<project_id>/data-resource?experiment_id=<experiment_id>&run_id=<run_id>
```
* `project_id` - Path variable, ID of the project.
* `experiment_id` - *Optional* parameter, ID of the experiment.
* `run_id` - *Optional* parameter, ID of the run. Unused for documents of type `experiment`.

Keep in mind that if an `experiment` document is deleted, all related documents of types under it will also be deleted. As you'd expect, `project` documents will be unaffected, as they reside above `experiment`.

## UI end-points
A number of end-points are available and dedicated to the UI, featuring pagination and sorting of results.

Their functionality is practically identical to the end-points described above, so they are not listed here. They can be accessed by removing `api/` from the path.
