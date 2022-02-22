package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunDataSchema;
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.service.RunDataSchemaService;

@RestController
@RequestMapping(value = "/api/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunDataSchemaController {
    @Autowired
    private RunDataSchemaService service;

    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA + "/{id}")
    public ResponseEntity<RunDataSchema> findDocumentById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(service.findDocumentById(projectId, id));
    }

    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<List<RunDataSchema>> findDocuments(@PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId,
            @RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(service.findDocumentsByProjectId(projectId, experimentId, runId, search));
    }

    @PostMapping("/{projectId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<RunDataSchema> createDocument(@PathVariable String projectId, @RequestBody @Valid RunDataSchemaDTO request, Authentication authentication) {
        return ResponseEntity.ok(service.createDocument(projectId, request, authentication.getName()));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA + "/{id}")
    public ResponseEntity<RunDataSchema> updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid RunDataSchemaDTO request) {
        return ResponseEntity.ok(service.updateDocument(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA + "/{id}")
    public ResponseEntity<Void> deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
        service.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<Void> deleteDocuments(@PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId) {
        service.deleteDocumentsByProjectId(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
}