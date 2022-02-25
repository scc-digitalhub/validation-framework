package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
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
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ExperimentController {
    @Autowired
    private ExperimentService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT)
    public ResponseEntity<ExperimentDTO> create(@PathVariable String projectId, @RequestBody @Valid ExperimentDTO request) {
        return ResponseEntity.ok(service.createExperiment(projectId, request));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT)
    public ResponseEntity<List<ExperimentDTO>> find(
            @PathVariable String projectId,
            @RequestParam("experimentName") Optional<String> experimentName) {
        return ResponseEntity.ok(service.findExperiments(projectId, experimentName));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<ExperimentDTO> findById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(service.findExperimentById(projectId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<ExperimentDTO> update(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid ExperimentDTO request) {
        return ResponseEntity.ok(service.updateExperiment(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<Void> delete(@PathVariable String projectId, @PathVariable String id) {
        service.deleteExperiment(projectId, id);
        return ResponseEntity.ok().build();
    }
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}/" + ValidationStorageConstants.RUN)
    public ResponseEntity<RunDTO> createRun(
            @PathVariable String projectId,
            @PathVariable String id,
            @RequestBody @Valid RunDTO request) {
        return ResponseEntity.ok(service.createRun(projectId, id, request));
    }
    
}
