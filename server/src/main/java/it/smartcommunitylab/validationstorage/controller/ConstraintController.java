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
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.service.ConstraintService;
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ConstraintController {
    @Autowired
    private ExperimentService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.CONSTRAINT)
    public ResponseEntity<ConstraintDTO> create(@PathVariable String projectId, @PathVariable String experimentId, @RequestBody @Valid ConstraintDTO request) {
        return ResponseEntity.ok(service.createConstraint(projectId, experimentId, request));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.CONSTRAINT)
    public ResponseEntity<List<ConstraintDTO>> find(@PathVariable String projectId, @PathVariable String experimentId) {
        return ResponseEntity.ok(service.findConstraints(projectId, experimentId));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.CONSTRAINT + "/{id}")
    public ResponseEntity<ConstraintDTO> findById(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String id) {
        return ResponseEntity.ok(service.findConstraintById(projectId, experimentId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.CONSTRAINT + "/{id}")
    public ResponseEntity<ConstraintDTO> update(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String id,
            @RequestBody @Valid ConstraintDTO request) {
        return ResponseEntity.ok(service.updateConstraint(projectId, experimentId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.CONSTRAINT + "/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String id) {
        service.deleteConstraint(projectId, experimentId, id);
        return ResponseEntity.ok().build();
    }
}
