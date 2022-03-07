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
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.service.RunMetadataService;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunMetadataController {
    @Autowired
    private RunService service;

    @PostMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_METADATA)
    public ResponseEntity<RunMetadataDTO> create(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @RequestBody @Valid RunMetadataDTO request) {
        return ResponseEntity.ok(service.createRunMetadata(projectId, experimentId, runId, request));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_METADATA)
    public ResponseEntity<RunMetadataDTO> find(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(service.findRunMetadata(projectId, experimentId, runId));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_METADATA)
    public ResponseEntity<RunMetadataDTO> update(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @RequestBody @Valid RunMetadataDTO request) {
        return ResponseEntity.ok(service.updateRunMetadata(projectId, experimentId, runId, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_METADATA)
    public ResponseEntity<Void> delete(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        service.deleteRunMetadata(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
    
}