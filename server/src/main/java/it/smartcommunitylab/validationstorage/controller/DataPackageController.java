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
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.service.DataResourceService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class DataPackageController {
    @Autowired
    private DataResourceService service;
    
    @PostMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE)
    public ResponseEntity<DataPackageDTO> create(@PathVariable String projectId, @RequestBody @Valid DataPackageDTO request) {
        return ResponseEntity.ok(service.createDataPackage(projectId, request));
    }
    
    @PostMapping(ValidationStorageConstants.PATH_FRICTIONLESS + ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE)
    public ResponseEntity<DataPackageDTO> createFrictionless(@PathVariable String projectId, @RequestBody @Valid DataPackageDTO request) {
        return ResponseEntity.ok(service.createDataPackage(projectId, request));
    }
    
    @GetMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE)
    public ResponseEntity<List<DataPackageDTO>> find(@PathVariable String projectId) {
        return ResponseEntity.ok(service.findDataPackages(projectId));
    }
    
    @GetMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE + "/{id}")
    public ResponseEntity<DataPackageDTO> findById(@PathVariable String projectId, String id) {
        return ResponseEntity.ok(service.findDataPackageById(projectId, id));
    }
    
    @GetMapping(ValidationStorageConstants.PATH_FRICTIONLESS + ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE + "/{id}")
    public ResponseEntity<DataPackageDTO> findFrictionlessById(@PathVariable String projectId, String id) {
        return ResponseEntity.ok(service.findFrictionlessDataPackageById(projectId, id));
    }
    
    @PutMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE + "/{id}")
    public ResponseEntity<DataPackageDTO> update(@PathVariable String projectId, String id, @RequestBody @Valid DataPackageDTO request) {
        return ResponseEntity.ok(service.updateDataPackage(projectId, id, request));
    }
    
    @DeleteMapping(ValidationStorageConstants.PATH_PROJECT + "/{projectId}/" + ValidationStorageConstants.PACKAGE + "/{id}")
    public ResponseEntity<Void> delete(@PathVariable String projectId, @PathVariable String id) {
        service.deleteDataPackage(projectId, id);
        return ResponseEntity.ok().build();
    }
    
}
