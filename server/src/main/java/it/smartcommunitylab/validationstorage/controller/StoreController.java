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
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.service.DataResourceService;

@RestController
@RequestMapping(value = "/api/p/{projectId}/store")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class StoreController {
    @Autowired
    private DataResourceService service;
    
    @PostMapping
    public StoreDTO create(@PathVariable String projectId, @RequestBody @Valid StoreDTO request) {
        return service.createStore(projectId, request);
    }
    
    @GetMapping
    public List<StoreDTO> find(@PathVariable String projectId) {
        return service.findStores(projectId);
    }
    
    @GetMapping("/{id}")
    public StoreDTO findById(@PathVariable String projectId, @PathVariable String id) {
        return service.findStoreById(projectId, id);
    }

    @PutMapping("/{id}")
    public StoreDTO update(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid StoreDTO request) {
        return service.updateStore(projectId, id, request);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable String projectId, @PathVariable String id) {
        service.deleteStore(projectId, id);
    }
    
}
