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
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;
import it.smartcommunitylab.validationstorage.service.RunConfigService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunConfigController {
    @Autowired
    private ExperimentService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_CONFIG)
    public ResponseEntity<RunConfigDTO> create(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @RequestBody @Valid RunConfigDTO request) {
        return ResponseEntity.ok(service.createRunConfig(projectId, experimentId, request));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_CONFIG)
    public ResponseEntity<RunConfigDTO> find(
            @PathVariable String projectId,
            @PathVariable String experimentId) {
        return ResponseEntity.ok(service.findRunConfig(projectId, experimentId));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_CONFIG)
    public ResponseEntity<RunConfigDTO> update(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @RequestBody @Valid RunConfigDTO request) {
        return ResponseEntity.ok(service.updateRunConfig(projectId, experimentId, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_CONFIG)
    public ResponseEntity<Void> delete(
            @PathVariable String projectId,
            @PathVariable String experimentId) {
        service.deleteRunConfig(projectId, experimentId);
        return ResponseEntity.ok().build();
    }
}
