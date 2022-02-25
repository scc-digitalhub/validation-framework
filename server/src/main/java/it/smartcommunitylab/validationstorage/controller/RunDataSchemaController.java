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
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.model.dto.SchemaResultDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunDataSchemaController {
    @Autowired
    private RunService service;

    @PostMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<SchemaResultDTO> create(
            @PathVariable String projectId,
            @PathVariable String runId,
            @RequestBody @Valid SchemaResultDTO request) {
        
        SchemaResultDTO response = new SchemaResultDTO();
        response.setReports(service.createRunDataSchemas(projectId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<SchemaResultDTO> find(
            @PathVariable String projectId,
            @PathVariable String runId) {
        
        SchemaResultDTO response = new SchemaResultDTO();
        response.setReports(service.findRunDataSchemas(projectId, runId));
        response.setResult(service.findSchemaResult(projectId, runId));
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA + "/{id}")
    public ResponseEntity<RunDataSchemaDTO> findById(
            @PathVariable String projectId,
            @PathVariable String runId,
            @PathVariable String id) {
        
        return ResponseEntity.ok(service.findRunDataSchemaById(projectId, runId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<SchemaResultDTO> update(
            @PathVariable String projectId,
            @PathVariable String runId,
            @RequestBody @Valid SchemaResultDTO request) {
        
        SchemaResultDTO response = new SchemaResultDTO();
        response.setReports(service.updateRunDataSchemas(projectId, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_DATA_SCHEMA)
    public ResponseEntity<Void> delete(
            @PathVariable String projectId,
            @PathVariable String runId) {
        service.deleteRunDataSchemas(projectId, runId);
        return ResponseEntity.ok().build();
    }
    
}