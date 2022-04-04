package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ExperimentController {
    @Autowired
    private ExperimentService service;

    @PostMapping
    public ExperimentDTO create(
            @PathVariable String projectId,
            @RequestBody @Valid ExperimentDTO request) {
        return service.createExperiment(projectId, request);
    }

    @GetMapping
    public List<ExperimentDTO> find(
            @PathVariable String projectId) {
        return service.findExperiments(projectId);
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
