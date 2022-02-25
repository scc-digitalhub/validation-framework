package it.smartcommunitylab.validationstorage.controller;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.dto.ProfileResultDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataProfileDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunDataProfileController {
    @Autowired
    private RunService service;

    @PostMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_PROFILE)
    public ResponseEntity<ProfileResultDTO> create(
            @PathVariable String projectId,
            @PathVariable String runId,
            @RequestBody @Valid ProfileResultDTO request) {
        
        ProfileResultDTO response = new ProfileResultDTO();
        response.setReports(service.createRunDataProfiles(projectId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_PROFILE)
    public ResponseEntity<ProfileResultDTO> find(
            @PathVariable String projectId,
            @PathVariable String runId) {
        
        ProfileResultDTO response = new ProfileResultDTO();
        response.setReports(service.findRunDataProfiles(projectId, runId));
        response.setResult(service.findProfileResult(projectId, runId));
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_PROFILE + "/{id}")
    public ResponseEntity<RunDataProfileDTO> findById(
            @PathVariable String projectId,
            @PathVariable String runId,
            @PathVariable String id) {
        
        return ResponseEntity.ok(service.findRunDataProfileById(projectId, runId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_PROFILE)
    public ResponseEntity<ProfileResultDTO> update(
            @PathVariable String projectId,
            @PathVariable String runId,
            @RequestBody @Valid ProfileResultDTO request) {
        
        ProfileResultDTO response = new ProfileResultDTO();
        response.setReports(service.updateRunDataProfiles(projectId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_PROFILE)
    public ResponseEntity<Void> delete(
            @PathVariable String projectId,
            @PathVariable String runId) {
        service.deleteRunDataProfiles(projectId, runId);
        return ResponseEntity.ok().build();
    }
}