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
import it.smartcommunitylab.validationstorage.model.dto.ProfileResultDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataProfileDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentName}/run/{runId}/data-profile")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunDataProfileController {
    @Autowired
    private RunService service;

    @PostMapping
    public ProfileResultDTO create(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @RequestBody @Valid ProfileResultDTO request) {
        
        ProfileResultDTO response = new ProfileResultDTO();
        response.setReports(service.createRunDataProfiles(projectId, experimentName, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return response;
    }
    
    @GetMapping
    public ProfileResultDTO find(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId) {
        
        ProfileResultDTO response = new ProfileResultDTO();
        response.setReports(service.findRunDataProfiles(projectId, experimentName, runId));
        response.setResult(service.findProfileResult(projectId, experimentName, runId));
        
        return response;
    }
    
    @GetMapping("/{id}")
    public RunDataProfileDTO findById(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @PathVariable String id) {
        
        return service.findRunDataProfileById(projectId, experimentName, runId, id);
    }

    @PutMapping
    public ProfileResultDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId,
            @RequestBody @Valid ProfileResultDTO request) {
        
        ProfileResultDTO response = new ProfileResultDTO();
        response.setReports(service.updateRunDataProfiles(projectId, experimentName, runId, request.getResult(), request.getReports()));
        response.setResult(request.getResult());
        
        return response;
    }

    @DeleteMapping
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            @PathVariable String runId) {
        service.deleteRunDataProfiles(projectId, experimentName, runId);
    }
}