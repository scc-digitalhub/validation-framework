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
import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.service.StoreService;

@RestController
@RequestMapping(value = "/api/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class StoreController {
    @Autowired
    private StoreService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.RUN_CONFIG)
    public ResponseEntity<Store> create(@PathVariable String projectId, @RequestBody @Valid StoreDTO request, Authentication authentication) {
        return ResponseEntity.ok(service.create(projectId, request, authentication.getName()));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN_CONFIG)
    public ResponseEntity<List<Store>> findByProjectId(
            @PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId,
            @RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(service.findByProjectId(projectId, experimentId, runId, search));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN_CONFIG + "/{id}")
    public ResponseEntity<Store> findById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(service.findById(projectId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.RUN_CONFIG + "/{id}")
    public ResponseEntity<Store> update(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid StoreDTO request) {
        return ResponseEntity.ok(service.update(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN_CONFIG + "/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable String projectId, @PathVariable String id) {
        service.deleteById(projectId, id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RESOURCE)
    public ResponseEntity<Void> deleteByProjectId(
            @PathVariable String projectId,
            @RequestParam("experimentId") Optional<String> experimentId,
            @RequestParam("runId") Optional<String> runId) {
        service.deleteByProjectId(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
}
