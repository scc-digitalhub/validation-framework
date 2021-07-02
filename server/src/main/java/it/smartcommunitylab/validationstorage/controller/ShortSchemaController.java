package it.smartcommunitylab.validationstorage.controller;

import java.security.Principal;
import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ShortSchema;
import it.smartcommunitylab.validationstorage.model.dto.ShortSchemaDTO;
import it.smartcommunitylab.validationstorage.service.ShortSchemaService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/project")
@RequiredArgsConstructor
@PreAuthorize(ValidationStorageUtils.PREAUTH_PROJECTID)
public class ShortSchemaController {
    private final ShortSchemaService documentService;

    @GetMapping("/{projectId}/" + ValidationStorageUtils.SHORT_SCHEMA + "/{id}")
    public ResponseEntity<ShortSchema> findDocumentById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(documentService.findDocumentById(projectId, id));
    }

    @GetMapping("/{projectId}/" + ValidationStorageUtils.SHORT_SCHEMA)
    public ResponseEntity<List<ShortSchema>> findDocuments(@PathVariable String projectId,
            @RequestParam("experiment_id") Optional<String> experimentId,
            @RequestParam("run_id") Optional<String> runId,
            @RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(documentService.findDocumentsByProjectId(projectId, experimentId, runId, search));
    }

    @PostMapping("/{projectId}/" + ValidationStorageUtils.SHORT_SCHEMA)
    public ResponseEntity<ShortSchema> createDocument(@PathVariable String projectId, @RequestBody @Valid ShortSchemaDTO request, Principal principal) {
        return ResponseEntity.ok(documentService.createDocument(projectId, request, ValidationStorageUtils.getPrincipalName(principal)));
    }

    @PutMapping("/{projectId}/" + ValidationStorageUtils.SHORT_SCHEMA + "/{id}")
    public ResponseEntity<ShortSchema> updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid ShortSchemaDTO request) {
        return ResponseEntity.ok(documentService.updateDocument(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageUtils.SHORT_SCHEMA + "/{id}")
    public ResponseEntity<Void> deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
        documentService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageUtils.SHORT_SCHEMA)
    public ResponseEntity<Void> deleteDocuments(@PathVariable String projectId,
            @RequestParam("experiment_id") Optional<String> experimentId,
            @RequestParam("run_id") Optional<String> runId) {
        documentService.deleteDocumentsByProjectId(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
}