package it.smartcommunitylab.validationstorage.controller;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
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
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentName}/run/{runId}/validation-report")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunValidationReportController {
    @Autowired
    private RunService service;

    @PostMapping
    public ValidationResultDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @RequestBody @Valid ValidationResultDTO request) {
        
        ValidationResultDTO response = new ValidationResultDTO();
        response.setReports(service.createRunValidationReports(projectId, experimentName, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return response;
    }
    
    @GetMapping
    public ValidationResultDTO find(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId) {
        
        ValidationResultDTO response = new ValidationResultDTO();
        response.setReports(service.findRunValidationReports(projectId, experimentName, runId));
        response.setResult(service.findValidationResult(projectId, experimentName, runId));
        
        return response;
    }
    
    @GetMapping("/{id}")
    public RunValidationReportDTO findById(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @PathVariable String id) {
        
        return service.findRunValidationReportById(projectId, experimentName, runId, id);
    }

    @PutMapping
    public ValidationResultDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @RequestBody @Valid ValidationResultDTO request) {
        
        ValidationResultDTO response = new ValidationResultDTO();
        response.setReports(service.updateRunValidationReports(projectId, experimentName, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return response;
    }

    @DeleteMapping
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId) {
        service.deleteRunValidationReports(projectId, experimentName, runId);
    }
    
}