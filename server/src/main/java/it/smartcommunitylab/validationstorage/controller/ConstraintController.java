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
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentId}/constraint")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class ConstraintController {
    @Autowired
    private ExperimentService service;
    
    @PostMapping
    public ConstraintDTO create(@PathVariable String projectId, @PathVariable String experimentId, @RequestBody @Valid ConstraintDTO request) {
        return service.createConstraint(projectId, experimentId, request);
    }
    
    @GetMapping
    public List<ConstraintDTO> find(@PathVariable String projectId, @PathVariable String experimentId) {
        return service.findConstraints(projectId, experimentId);
    }
    
    @GetMapping("/{id}")
    public ConstraintDTO findById(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String id) {
        return service.findConstraintById(projectId, experimentId, id);
    }

    @PutMapping("/{id}")
    public ConstraintDTO update(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String id,
            @RequestBody @Valid ConstraintDTO request) {
        return service.updateConstraint(projectId, experimentId, id, request);
    }

    @DeleteMapping("/{id}")
    public void delete(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String id) {
        service.deleteConstraint(projectId, experimentId, id);
    }
}
