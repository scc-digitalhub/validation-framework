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
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentName}/run")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunController {
    @Autowired
    private RunService service;
    
    @PostMapping
    public RunDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @RequestBody @Valid RunDTO request) {
        return service.createRun(projectId, experimentName, request);
    }
    
    @GetMapping
    public List<RunDTO> find(
            @PathVariable String projectId,
            @PathVariable String experimentName) {
        return service.findRuns(projectId, experimentName);
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
