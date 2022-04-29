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

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class BaseRunController {
    @Autowired
    protected RunService service;
    
    @PostMapping
    public RunDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @RequestBody(required=false) @Valid RunDTO request) {
        return service.createRun(projectId, experimentName, request);
    }
    
    @GetMapping("/{id}")
    public RunDTO findById(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String id) {
        return service.findRunById(projectId, experimentName, id);
    }
    
    @PutMapping("/{id}")
    public RunDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String id,
            @RequestBody @Valid RunDTO request) {
        return service.updateRun(projectId, experimentName, id, request);
    }

    @DeleteMapping("/{id}")
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String id) {
        service.deleteRun(projectId, experimentName, id);
    }
    
}
