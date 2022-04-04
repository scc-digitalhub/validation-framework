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
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentName}/run-config")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunConfigController {
    @Autowired
    private ExperimentService service;
    
    @PostMapping
    public RunConfigDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @RequestBody @Valid RunConfigDTO request) {
        return service.createExperimentRunConfig(projectId, experimentName, request);
    }
    
    @GetMapping
    public RunConfigDTO find(
            @PathVariable String projectId,
            @PathVariable String experimentName) {
        return service.findExperimentRunConfig(projectId, experimentName);
    }

    @PutMapping
    public RunConfigDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @RequestBody @Valid RunConfigDTO request) {
        return service.updateExperimentRunConfig(projectId, experimentName, request);
    }

    @DeleteMapping
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentName) {
        service.deleteExperimentRunConfig(projectId, experimentName);
    }
}
