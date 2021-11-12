## Requirements

The back-end needs access to a *MongoDB* database to store documents into. Make sure you have an instance available, either locally or remotely.

## Running with Docker
Docker is the easiest way to launch an instance that contains both the back-end and the UI. If you do not have access to Docker, skip this section and move to [Configuration](#configuration).

In the root folder is a `server.env.template` file: make a duplicate and rename it to just `server.env`.
Within are some environment variables you need to change:

`MONGODB_URI`: URI to the MongoDB instance. It has to follow the format `mongodb://<username>:<password>@<address>:<port>/<database>?authSource=<authentication_database>`
* `<username>`: User name
* `<password>`: Password
* `<address>`: Address of the MongoDB instance
* `<port>`: Port of the MongoDB instance (usually `27017`)
* `<database>`: The database to use
* `<authentication_database>`: The database for user credentials within MongoDB (usually `admin`)

`CLIENT_ID`: Client ID within AAC for this app.

`CLIENT_SECRET`: Client secret within AAC for this app.

`ISSUER_URI`: The AAC instance you intend to use for OAuth2.

Build the image:
```
docker build -t validation .
```

Run a container:
```
docker run --name validation --env-file server.env -p 8200:8200 -t validation
```

The UI can now be accessed at `localhost:8200`.

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
The UI can also be packaged with the back-end, provided it is configured, built and the resulting files are moved to the appropriate path.

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
localhost:8200/api/project/<projectId>
```
* `projectId` - Path variable, ID of the project.

---

#### Update a project (PUT):
```
localhost:8200/api/project/<projectId>
```
* `projectId` - Path variable, ID of the project.

Contents of the body:
* `id` -*Optional*, ID of the project. This value can't actually be updated. If specified, the back-end will check that it matches the `projectId` specified as path variable. Consider this an extra measure to ensure you're updating the correct document.
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
localhost:8200/api/project/<projectId>
```
* `projectId` - Path variable, ID of the project.
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
localhost:8200/api/project/<projectId>/experiment
```
* `projectId` - Path variable, ID of the project.

Contents of the body:
* `experimentId` -**Mandatory**, ID of the experiment. Note it is only unique within the project it belongs to.
* `experimentName` - *Optional*, name of the experiment.

Example:
```
{
  "experimentId": "exp1",
  "experimentName": "Exp 1"
}
```

#### run-metadata
```
localhost:8200/api/project/<projectId>/run-metadata?overwrite=<true_or_false>
```
* `projectId` - Path variable, ID of the project.
* `overwrite` - *Optional* parameter, boolean.

Contents of the body:
* `experimentId` - **Mandatory**, ID of the experiment.
* `runId` - **Mandatory** ID of the run. Note it is only unique within the project and experiment it belongs to.
* `experimentName` - *Optional*, name of the experiment.
* `contents` - *Optional*, any object, can contain any valid JSON.

Example:
```
{
  "experimentId": "exp1",
	"experimentName": "Exp 1",
	"runId": "run1",
	"contents": {
		"a":"aaa",
		"b":"bbb"
	}
}
```

This document represents a run, which is why it presents a `overwrite` parameter.

If `overwrite` is specified and set to `true`, it will generate the document and delete (if found) the previous `run-metadata` document that matches the same combination of `projectId`, `experimentId` and `runId`.

All documents of other types that match this combination will also be deleted. As you'd expect, `project` and `experiment` documents will be unaffected, as they reside above `run-metadata`.

If `overwrite` is not specified, or set to `false`, and a document with the same `projectId`, `experimentId` and `runId` already exists, it will just result in an error.

#### artifact-metadata
```
localhost:8200/api/project/<projectId>/artifact-metadata
```
* `projectId` - Path variable, ID of the project.

Contents of the body:
* `experimentId` - **Mandatory**, ID of the experiment.
* `runId` - **Mandatory**, ID of the run.
* `name` - **Mandatory**, name of the file.
* `uri` - **Mandatory**, location of the file.
* `experimentName` - *Optional*, name of the experiment.

Example:
```
{
  "experimentId":"experiment_validation",
  "runId":"c51dbaf523e943c099b11a53a38e6a4f",
  "name": "file.sample",
  "uri":"a/b/c"
}
```

No error will occur for `artifact-metadata` if other documents contain the same combination of values.

#### data-profile, data-resource, run-environment, short-report, short-schema
```
localhost:8200/api/project/<projectId>/<document-type>
```
* `projectId` - Path variable, ID of the project.
* `document-type` - Path variable, `data-profile`, `data-resource`, `run-environment`, `short-report` or `short-schema`. These documents behave identically.

Contents of the body:
* `experimentId` - **Mandatory**, ID of the experiment.
* `runId` - **Mandatory**, ID of the run.
* `experimentName` - *Optional*, name of the experiment.
* `contents` - *Optional*, any object, can contain any valid JSON.

Example:
```
{
  "experimentId": "exp1",
  "experimentName": "some_experiment",
  "runId": "run1",
  "contents": {
    "a":"aaa",
    "b":"bbb"
  }
}
```

If a document already exists with the same `projectId`, `experimentId` and `runId`, it will result in an error.

---

### Get document by ID (GET):

```
localhost:8200/api/project/<projectId>/data-resource/<documentId>
```
* `projectId` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `documentId` - Path variable, ID of the document you wish to retrieve.

---

### Get documents by project ID (GET)
```
localhost:8200/api/project/<projectId>/data-resource?experimentId=<experimentId>&runId=<runId>&search=<search>
```
* `projectId` - Path variable, ID of the project.
* `experimentId` - *Optional* parameter, ID of the experiment.
* `runId` - *Optional* parameter, ID of the run. Unused for documents of type `experiment`.
* `search` - *Optional* parameter, a case-insensitive, diacritics-insensitive keyword to filter results by. Looks for a match in the `experimentName` field of entries. For `artifact-metadata` documents only, the match may also be found in the `name` field instead.

---

### Update document (PUT)
```
localhost:8200/api/project/<projectId>/data-resource/<documentId>
```
* `projectId` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `documentId` - Path variable, ID of the document you wish to update.

The content of the body follows the same structure as the endpoint for creation, but no fields are mandatory.

For any document except `artifact-metadata`: `experimentId` and `runId` cannot be changed, but if specified, the back-end will check that they indeed match the values of the document with the specified ID, and return an error if they don't.

---

### Delete document by ID (DELETE)
```
localhost:8200/api/project/<projectId>/data-resource/<documentId>
```
* `projectId` - Path variable, ID of the project the document belongs to. If it does not match the project ID contained in the document, it will result in error.
* `documentId` - Path variable, ID of the document you wish to delete.

Keep in mind that if an `experiment` document is deleted, all related documents of types under it will also be deleted. As you'd expect, `project` documents will be unaffected, as they reside above `experiment`.

---

### Delete documents by project ID (DELETE)
```
localhost:8200/api/project/<projectId>/data-resource?experimentId=<experimentId>&runId=<runId>
```
* `projectId` - Path variable, ID of the project.
* `experimentId` - *Optional* parameter, ID of the experiment.
* `runId` - *Optional* parameter, ID of the run. Unused for documents of type `experiment`.

Keep in mind that if an `experiment` document is deleted, all related documents of types under it will also be deleted. As you'd expect, `project` documents will be unaffected, as they reside above `experiment`.

## UI end-points
A number of end-points featuring pagination and sorting of results are available and dedicated to the UI. Their functionality is practically identical to the end-points described above.

The path for these end-points is however different: `api/` is not present and documents are generally identified by a combination of `projectId`, `experimentId` and `runId`, instead of the document's own ID.

For example, to get a `run-metadata` document, instead of:
```
localhost:8200/api/project/<projectId>/run-metadata/<documentId>
```
The end-point for the UI is:
```
localhost:8200/project/<projectId>/experiment/<experimentId>/run/<runId>/run-metadata
```

There are no end-points for creating and updating documents outside of `project`.

### run-summary
The UI also makes use of another document, the `run-summary`: this is not actually persisted in the database, as it is built on-the-fly, using the `run-metadata` document as reference, but combining information from other documents as well, so that a summary of the run's information becomes available with a single API call.

It has an end-point for deletion, which deletes all documents related to the run. Here are brief descriptions of the end-points.

#### List basic run summaries
```
localhost:8200/project/<projectId>/experiment/<experimentId>/run
```
* `projectId` - Path variable, ID of the project.
* `experimentId` - Path variable, ID of the experiment.

Generates and returns `run-summary` documents for all runs under the specified experiment. These documents contain information from `run-metadata` and `short-report` documents.

#### Retrieve basic run summary
```
localhost:8200/project/<projectId>/experiment/<experimentId>/run/<runId>
```
* `projectId` - Path variable, ID of the project.
* `experimentId` - Path variable, ID of the experiment.
* `runId` - Path variable, ID of the run.

Generates and returns a `run-summary` document for the specified run, containing information from `run-metadata` and `short-report` documents.

#### Retrieve recent rich run summaries
```
localhost:8200/project/<projectId>/experiment/<experimentId>/run-rich-recent
```
* `projectId` - Path variable, ID of the project.
* `experimentId` - Path variable, ID of the experiment.

Generates and returns a number `run-summary` documents under the specified experiment, for only the most recent runs. They contain information from `run-metadata`, `short-report` and `data-profile` documents.


#### Retrieve rich run summaries by run-metadata IDs
```
localhost:8200/project/<projectId>/experiment/<experimentId>/run-rich/<list_of_run-metadata_ids>
```
* `projectId` - Path variable, ID of the project.
* `experimentId` - Path variable, ID of the experiment.
* `list_of_run-metadata_ids` - Path variable, comma-separated list of `run-metadata` document IDs.

Generates and returns a list of `run-summary` documents for the specified runs. They contain information from `run-metadata`, `short-report` and `data-profile` documents. Note that runs must be identified by the `run-metadata` document's ID, not the run's ID.

#### Delete all documents related to a run
```
localhost:8200/project/<projectId>/run/<run-metadata_id>
```
* `projectId` - Path variable, ID of the project.
* `run-metadata_id` - Path variable, `run-metadata` document ID.

Deletes all document related to the run identified by the provided `run-metadata` document ID.
