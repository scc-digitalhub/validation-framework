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
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@RestController
@RequestMapping(value = "/api/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ExperimentController {
    @Autowired
    private ExperimentService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT)
    public ResponseEntity<Experiment> create(@PathVariable String projectId, @RequestBody @Valid ExperimentDTO request, Authentication authentication) {
        return ResponseEntity.ok(service.create(projectId, request, authentication.getName()));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT)
    public ResponseEntity<List<Experiment>> findByProjectId(
            @PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId,
            @RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(service.findByProjectId(projectId, experimentId, runId, search));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<Experiment> findById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(service.findById(projectId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<Experiment> update(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid ExperimentDTO request) {
        return ResponseEntity.ok(service.update(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable String projectId, @PathVariable String id) {
        service.deleteById(projectId, id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT)
    public ResponseEntity<Void> deleteByProjectId(
            @PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId) {
        service.deleteByProjectId(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
}
