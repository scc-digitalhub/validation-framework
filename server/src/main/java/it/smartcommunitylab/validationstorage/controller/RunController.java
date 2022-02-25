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
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.service.RunService;

@RestController
@RequestMapping(value = ValidationStorageConstants.ENDPOINT_ROOT + ValidationStorageConstants.PATH_PROJECT)
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunController {
    @Autowired
    private RunService service;
    
    @PostMapping("/{projectId}/" + ValidationStorageConstants.RUN)
    public ResponseEntity<RunDTO> create(@PathVariable String projectId, @RequestBody @Valid RunDTO request) {
        return ResponseEntity.ok(service.createRun(projectId, request));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN)
    public ResponseEntity<List<RunDTO>> find(
            @PathVariable String projectId,
            @RequestParam("experimentName") Optional<String> experimentName) {
        return ResponseEntity.ok(service.findRuns(projectId, experimentName));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{id}")
    public ResponseEntity<RunDTO> findById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(service.findRunById(projectId, id));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{id}")
    public ResponseEntity<Void> delete(@PathVariable String projectId, @PathVariable String id) {
        service.deleteRun(projectId, id);
        return ResponseEntity.ok().build();
    }
    
}
