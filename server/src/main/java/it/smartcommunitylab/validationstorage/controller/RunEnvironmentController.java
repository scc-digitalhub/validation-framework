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
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.service.RunEnvironmentService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/project")
@RequiredArgsConstructor
@PreAuthorize(ValidationStorageUtils.PREAUTH_PROJECTID)
public class RunEnvironmentController {
	private final RunEnvironmentService documentService;
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.RUN_ENVIRONMENT + "/{id}")
	public ResponseEntity<RunEnvironment> findDocumentById(@PathVariable String projectId, @PathVariable String id) {
		return ResponseEntity.ok(documentService.findDocumentById(projectId, id));
	}
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.RUN_ENVIRONMENT)
	public ResponseEntity<List<RunEnvironment>> findDocuments(@PathVariable String projectId,
															@RequestParam("experiment_id") Optional<String> experimentId,
															@RequestParam("run_id") Optional<String> runId,
															@RequestParam("search") Optional<String> search) {
		return ResponseEntity.ok(documentService.findDocumentsByProjectId(projectId, experimentId, runId, search));
	}
	
	@PostMapping("/{projectId}/" + ValidationStorageUtils.RUN_ENVIRONMENT)
	public ResponseEntity<RunEnvironment> createDocument(@PathVariable String projectId, @RequestBody @Valid RunEnvironmentDTO request, Principal principal) {
		return ResponseEntity.ok(documentService.createDocument(projectId, request, ValidationStorageUtils.getPrincipalName(principal)));
	}
	
	@PutMapping("/{projectId}/" + ValidationStorageUtils.RUN_ENVIRONMENT + "/{id}")
	public ResponseEntity<RunEnvironment> updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody @Valid RunEnvironmentDTO request) {
		return ResponseEntity.ok(documentService.updateDocument(projectId, id, request));
	}
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.RUN_ENVIRONMENT + "/{id}")
	public ResponseEntity<Void> deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
		documentService.deleteDocumentById(projectId, id);
		return ResponseEntity.ok().build();
	}
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.RUN_ENVIRONMENT)
	public ResponseEntity<Void> deleteDocuments(@PathVariable String projectId,
												@RequestParam("experiment_id") Optional<String> experimentId,
												@RequestParam("run_id") Optional<String> runId) {
		documentService.deleteDocumentsByProjectId(projectId, experimentId, runId);
		return ResponseEntity.ok().build();
	}
}