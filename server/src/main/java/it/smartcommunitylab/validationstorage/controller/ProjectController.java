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
    private ProjectService documentService;

    @PreAuthorize("permitAll()")
    @GetMapping
    public ResponseEntity<List<Project>> findDocuments() {
        return ResponseEntity.ok(documentService.findDocuments());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Project> findDocumentById(@PathVariable String id) {
        return ResponseEntity.ok(documentService.findDocumentById(id));
    }

    @PreAuthorize(ValidationStorageConstants.PREAUTH_REQUEST_ID)
    @PostMapping
    public ResponseEntity<Project> createDocument(@RequestBody @Valid ProjectDTO request, Authentication authentication) {
        return ResponseEntity.ok(documentService.createDocument(request, authentication.getName()));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Project> updateDocument(@PathVariable String id, @RequestBody @Valid ProjectDTO request) {
        return ResponseEntity.ok(documentService.updateDocument(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDocumentById(@PathVariable String id) {
        documentService.deleteDocumentById(id);
        return ResponseEntity.ok().build();
    }
}
