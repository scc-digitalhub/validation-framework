package it.smartcommunitylab.validationstorage.controller;

import java.util.List;

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
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.service.ProjectService;

@RestController
@RequestMapping(value = "/api/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_ID)
public class ProjectController {
    @Autowired
    private ProjectService service;
    
    @PreAuthorize(ValidationStorageConstants.PREAUTH_REQUEST_ID)
    @PostMapping
    public ResponseEntity<Project> create(@RequestBody @Valid ProjectDTO request, Authentication authentication) {
        return ResponseEntity.ok(service.create(request, authentication.getName()));
    }
    
    @PreAuthorize("permitAll()")
    @GetMapping
    public ResponseEntity<List<Project>> find() {
        return ResponseEntity.ok(service.find());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Project> findById(@PathVariable String id) {
        return ResponseEntity.ok(service.findById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Project> update(@PathVariable String id, @RequestBody @Valid ProjectDTO request) {
        return ResponseEntity.ok(service.update(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable String id) {
        service.deleteById(id);
        return ResponseEntity.ok().build();
    }
}
