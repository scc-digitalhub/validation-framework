package it.smartcommunitylab.validationstorage.controller;

import java.security.Principal;
import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.http.ResponseEntity;
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

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.service.ExperimentService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/project")
@RequiredArgsConstructor
@PreAuthorize(ValidationStorageUtils.PREAUTH_PROJECTID)
public class ExperimentController {

    private final ExperimentService documentService;

    @GetMapping("/{projectId}/" + ValidationStorageUtils.EXPERIMENT + "/{id}")
    public ResponseEntity<Experiment> findDocumentById(@PathVariable String projectId, @PathVariable String id) {
        return ResponseEntity.ok(documentService.findDocumentById(projectId, id));
    }

    @GetMapping("/{projectId}/" + ValidationStorageUtils.EXPERIMENT)
    public ResponseEntity<List<Experiment>> findDocuments(@PathVariable String projectId,
            @RequestParam("experiment_id") Optional<String> experimentId,
            @RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(documentService.findDocumentsByProjectId(projectId, experimentId, search));
    }

    @PostMapping("/{projectId}/" + ValidationStorageUtils.EXPERIMENT)
    public ResponseEntity<Experiment> createDocument(@PathVariable String projectId, @RequestBody @Valid ExperimentDTO request, Principal principal) {
        return ResponseEntity.ok(documentService.createDocument(projectId, request, ValidationStorageUtils.getPrincipalName(principal)));
    }

    @PutMapping("/{projectId}/" + ValidationStorageUtils.EXPERIMENT + "/{id}")
    public ResponseEntity<Experiment> updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid ExperimentDTO request) {
        return ResponseEntity.ok(documentService.updateDocument(projectId, id, request));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageUtils.EXPERIMENT + "/{id}")
    public ResponseEntity<Void> deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
        documentService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageUtils.EXPERIMENT)
    public ResponseEntity<Void> deleteDocuments(@PathVariable String projectId,
            @RequestParam("experiment_id") Optional<String> experimentId) {
        documentService.deleteDocumentsByProjectId(projectId, experimentId);
        return ResponseEntity.ok().build();
    }
}
