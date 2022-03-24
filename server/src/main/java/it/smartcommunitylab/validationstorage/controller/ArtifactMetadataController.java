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
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentId}/run/{runId}/artifact-metadata")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ArtifactMetadataController {
    @Autowired
    private RunService service;
    
    @PostMapping
    public ArtifactMetadataDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @RequestBody @Valid ArtifactMetadataDTO request) {
        return service.createArtifactMetadata(projectId, experimentId, runId, request);
    }

    @GetMapping
    public List<ArtifactMetadataDTO> find(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return service.findArtifactMetadata(projectId, experimentId, runId);
    }
    
    @GetMapping("/{id}")
    public ArtifactMetadataDTO findById(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @PathVariable String id) {
        return service.findArtifactMetadataById(projectId, experimentId, runId, id);
    }

    @PutMapping("/{id}")
    public ArtifactMetadataDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @PathVariable String id,
            @RequestBody @Valid ArtifactMetadataDTO request) {
        return service.updateArtifactMetadata(projectId, experimentId, runId, id, request);
    }
    
    @DeleteMapping("/{id}")
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @PathVariable String id) {
        service.deleteArtifactMetadata(projectId, experimentId, runId, id);
    }
}