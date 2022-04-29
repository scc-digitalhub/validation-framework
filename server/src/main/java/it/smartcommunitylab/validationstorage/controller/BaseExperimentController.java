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
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class BaseExperimentController {
    @Autowired
    protected ExperimentService service;

    @PostMapping
    public ExperimentDTO create(
            @PathVariable String projectId,
            @RequestBody @Valid ExperimentDTO request) {
        return service.createExperiment(projectId, request);
    }

    @GetMapping("/{name}")
    public ExperimentDTO findByName(
            @PathVariable String projectId,
            @PathVariable String name) {
        return service.findExperimentByName(projectId, name);
    }

    @PutMapping("/{name}")
    public ExperimentDTO update(
            @PathVariable String projectId,
            @PathVariable String name,
            @RequestBody @Valid ExperimentDTO request) {
        return service.updateExperiment(projectId, name, request);
    }

    @DeleteMapping("/{name}")
    public void delete(
            @PathVariable String projectId,
            @PathVariable String name) {
        service.deleteExperiment(projectId, name);
    }

}
