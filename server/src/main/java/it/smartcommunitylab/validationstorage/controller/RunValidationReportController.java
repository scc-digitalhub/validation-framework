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
import it.smartcommunitylab.validationstorage.model.dto.RunValidationReportDTO;
import it.smartcommunitylab.validationstorage.model.dto.ValidationResultDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunValidationReportController {
    @Autowired
    private RunService service;

    @PostMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_VALIDATION_REPORT)
    public ResponseEntity<ValidationResultDTO> create(
            @PathVariable String projectId,
            @PathVariable String runId,
            @RequestBody @Valid ValidationResultDTO request) {
        
        ValidationResultDTO response = new ValidationResultDTO();
        response.setReports(service.createRunValidationReports(projectId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_VALIDATION_REPORT)
    public ResponseEntity<ValidationResultDTO> find(
            @PathVariable String projectId,
            @PathVariable String runId) {
        
        ValidationResultDTO response = new ValidationResultDTO();
        response.setReports(service.findRunValidationReports(projectId, runId));
        response.setResult(service.findValidationResult(projectId, runId));
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_VALIDATION_REPORT + "/{id}")
    public ResponseEntity<RunValidationReportDTO> findById(
            @PathVariable String projectId,
            @PathVariable String runId,
            @PathVariable String id) {
        
        return ResponseEntity.ok(service.findRunValidationReportById(projectId, runId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_VALIDATION_REPORT)
    public ResponseEntity<ValidationResultDTO> update(
            @PathVariable String projectId,
            @PathVariable String runId,
            @RequestBody @Valid ValidationResultDTO request) {
        
        ValidationResultDTO response = new ValidationResultDTO();
        response.setReports(service.updateRunValidationReports(projectId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_VALIDATION_REPORT)
    public ResponseEntity<Void> delete(
            @PathVariable String projectId,
            @PathVariable String runId) {
        service.deleteRunValidationReports(projectId, runId);
        return ResponseEntity.ok().build();
    }
    
}