package it.smartcommunitylab.validationstorage.controller;

import java.util.List;

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
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.service.DataResourceService;

@RestController
@RequestMapping(value = "/api")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class DataPackageController {
    @Autowired
    private DataResourceService service;
    
    @PostMapping("/p/{projectId}/package")
    public DataPackageDTO create(
            @PathVariable String projectId,
            @RequestBody @Valid DataPackageDTO request) {
        return service.createDataPackage(projectId, request);
    }
    
    @PostMapping("/frictionless/p/{projectId}/package")
    public DataPackageDTO createFrictionless(
            @PathVariable String projectId,
            @RequestBody @Valid DataPackageDTO request) {
        return service.createDataPackage(projectId, request);
    }
    
    @GetMapping("/p/{projectId}/package")
    public List<DataPackageDTO> find(
            @PathVariable String projectId) {
        return service.findDataPackages(projectId);
    }
    
    @GetMapping("/p/{projectId}/package/{id}")
    public DataPackageDTO findById(
            @PathVariable String projectId,
            @PathVariable String id) {
        return service.findDataPackageById(projectId, id);
    }
    
    @GetMapping("/frictionless/p/{projectId}/package/{id}")
    public DataPackageDTO findFrictionlessById(
            @PathVariable String projectId,
            @PathVariable String id) {
        return service.findFrictionlessDataPackageById(projectId, id);
    }
    
    @PutMapping("/p/{projectId}/package/{id}")
    public DataPackageDTO update(
            @PathVariable String projectId,
            @PathVariable String id,
            @RequestBody @Valid DataPackageDTO request) {
        return service.updateDataPackage(projectId, id, request);
    }
    
    @DeleteMapping("/p/{projectId}/package/{id}")
    public void delete(
            @PathVariable String projectId,
            @PathVariable String id) {
        service.deleteDataPackage(projectId, id);
    }
    
}
