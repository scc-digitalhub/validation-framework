package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
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
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.service.ArtifactMetadataService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/artifact-metadata")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ArtifactMetadataController {
    @Autowired
    private ArtifactMetadataService documentService;

    @GetMapping("/{id}")
    public ArtifactMetadata findDocumentById(@PathVariable String projectId, @PathVariable String id) {
        return documentService.findDocumentById(projectId, id);
    }

    @GetMapping
    public List<ArtifactMetadata> findDocuments(@PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId,
            @RequestParam("search") Optional<String> search) {
        return documentService.findDocumentsByProjectId(projectId, experimentId, runId, search);
    }

    @PostMapping
    public ArtifactMetadata createDocument(@PathVariable String projectId, @RequestBody @Valid ArtifactMetadataDTO request, Authentication authentication) {
        return documentService.createDocument(projectId, request, authentication.getName());
    }

    @PutMapping("/{id}")
    public ArtifactMetadata updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid ArtifactMetadataDTO request) {
        return documentService.updateDocument(projectId, id, request);
    }

    @DeleteMapping("/{id}")
    public void deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
        documentService.deleteDocumentById(projectId, id);
    }

    @DeleteMapping
    public void deleteDocuments(@PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId) {
        documentService.deleteDocumentsByProjectId(projectId, experimentId, runId);
    }
}