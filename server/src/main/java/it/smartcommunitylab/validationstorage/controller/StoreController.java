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
import it.smartcommunitylab.validationstorage.service.DataResourceService;
import it.smartcommunitylab.validationstorage.service.StoreService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class StoreController {
    @Autowired
    private DataResourceService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.STORE)
    public ResponseEntity<StoreDTO> create(@PathVariable String projectId, @RequestBody @Valid StoreDTO request) {
        return ResponseEntity.ok(service.createStore(projectId, request));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.STORE)
    public ResponseEntity<List<StoreDTO>> find(@PathVariable String projectId) {
        return ResponseEntity.ok(service.findStores(projectId));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.STORE + "/{id}")
    public ResponseEntity<StoreDTO> findById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(service.findStoreById(projectId, id));
    }

    @PutMapping("/{projectId}/" + ValidationStorageConstants.STORE + "/{id}")
    public ResponseEntity<StoreDTO> update(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid StoreDTO request) {
        return ResponseEntity.ok(service.updateStore(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.STORE + "/{id}")
    public ResponseEntity<Void> delete(@PathVariable String projectId, @PathVariable String id) {
        service.deleteStore(projectId, id);
        return ResponseEntity.ok().build();
    }
    
}
