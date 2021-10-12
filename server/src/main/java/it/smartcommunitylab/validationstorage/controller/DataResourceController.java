package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

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
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.service.DataResourceService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/project")
@RequiredArgsConstructor
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class DataResourceController {
    private final DataResourceService documentService;

    @GetMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE + "/{id}")
    public ResponseEntity<DataResource> findDocumentById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(documentService.findDocumentById(projectId, id));
    }

    @GetMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE)
    public ResponseEntity<List<DataResource>> findDocuments(@PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId,
            @RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(documentService.findDocumentsByProjectId(projectId, experimentId, runId, search));
    }

    @PostMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE)
    public ResponseEntity<DataResource> createDocument(@PathVariable String projectId, @RequestBody @Valid DataResourceDTO request, Authentication authentication) {
        return ResponseEntity.ok(documentService.createDocument(projectId, request, ValidationStorageUtils.getAuthorName(authentication)));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE + "/{id}")
    public ResponseEntity<DataResource> updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid DataResourceDTO request) {
        return ResponseEntity.ok(documentService.updateDocument(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE + "/{id}")
    public ResponseEntity<Void> deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
        documentService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE)
    public ResponseEntity<Void> deleteDocuments(@PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId) {
        documentService.deleteDocumentsByProjectId(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
}