package it.smartcommunitylab.validationstorage.controller;

import java.util.List;

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
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.service.DataResourceService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class DataResourceController {
    @Autowired
    private DataResourceService service;
    
    @PostMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE)
    public ResponseEntity<DataResourceDTO> create(@PathVariable String projectId, @RequestBody @Valid DataResourceDTO request) {
        return ResponseEntity.ok(service.createDataResource(projectId, request));
    }
    
    @PostMapping(ValidationStorageConstants.PATH_FRICTIONLESS + ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE)
    public ResponseEntity<DataResourceDTO> createFrictionless(@PathVariable String projectId, @RequestBody @Valid DataResourceDTO request) {
        return ResponseEntity.ok(service.createDataResource(projectId, request));
    }
    
    @GetMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE)
    public ResponseEntity<List<DataResourceDTO>> find(@PathVariable String projectId) {
        return ResponseEntity.ok(service.findDataResources(projectId));
    }
    
    @GetMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE + "/{id}")
    public ResponseEntity<DataResourceDTO> findById(@PathVariable String projectId, String id) {
        return ResponseEntity.ok(service.findDataResourceById(projectId, id));
    }
    
    @GetMapping(ValidationStorageConstants.PATH_FRICTIONLESS + ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE + "/{id}")
    public ResponseEntity<DataResourceDTO> findFrictionlessById(@PathVariable String projectId, String id) {
        return ResponseEntity.ok(service.findFrictionlessDataResourceById(projectId, id));
    }
    
    @PutMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE + "/{id}")
    public ResponseEntity<DataResourceDTO> update(@PathVariable String projectId, String id, @RequestBody @Valid DataResourceDTO request) {
        return ResponseEntity.ok(service.updateDataResource(projectId, id, request));
    }
    
    @DeleteMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.RESOURCE + "/{id}")
    public ResponseEntity<Void> delete(@PathVariable String projectId, @PathVariable String id) {
        service.deleteDataResource(projectId, id);
        return ResponseEntity.ok().build();
    }
    
}
