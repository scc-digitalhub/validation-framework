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
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.model.dto.SchemaResultDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentId}/run/{runId}/data-schema")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunDataSchemaController {
    @Autowired
    private RunService service;

    @PostMapping
    public SchemaResultDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @RequestBody @Valid SchemaResultDTO request) {
        
        SchemaResultDTO response = new SchemaResultDTO();
        response.setReports(service.createRunDataSchemas(projectId, experimentId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return response;
    }
    
    @GetMapping
    public SchemaResultDTO find(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        
        SchemaResultDTO response = new SchemaResultDTO();
        response.setReports(service.findRunDataSchemas(projectId, experimentId, runId));
        response.setResult(service.findSchemaResult(projectId, experimentId, runId));
        
        return response;
    }
    
    @GetMapping("/{id}")
    public RunDataSchemaDTO findById(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @PathVariable String id) {
        
        return service.findRunDataSchemaById(projectId, experimentId, runId, id);
    }

    @PutMapping
    public SchemaResultDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            @RequestBody @Valid SchemaResultDTO request) {
        
        SchemaResultDTO response = new SchemaResultDTO();
        response.setReports(service.updateRunDataSchemas(projectId, experimentId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return response;
    }

    @DeleteMapping
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        service.deleteRunDataSchemas(projectId, experimentId, runId);
    }
    
}