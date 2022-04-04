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
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentName}/run/{runId}/environment")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunEnvironmentController {
    @Autowired
    private RunService service;

    @PostMapping
    public RunEnvironmentDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @RequestBody @Valid RunEnvironmentDTO request) {
        return service.createRunEnvironment(projectId, experimentName, runId, request);
    }
    
    @GetMapping
    public RunEnvironmentDTO find(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId) {
        return service.findRunEnvironment(projectId, experimentName, runId);
    }

    @PutMapping
    public RunEnvironmentDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @RequestBody @Valid RunEnvironmentDTO request) {
        return service.updateRunEnvironment(projectId, experimentName, runId, request);
    }

    @DeleteMapping
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId) {
        service.deleteRunEnvironment(projectId, experimentName, runId);
    }
    
}