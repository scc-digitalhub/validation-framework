package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import org.springframework.http.ResponseEntity;
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
import it.smartcommunitylab.validationstorage.model.DataProfile;
import it.smartcommunitylab.validationstorage.model.dto.DataProfileDTO;
import it.smartcommunitylab.validationstorage.service.DataProfileService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/project")
@RequiredArgsConstructor
public class DataProfileController {
	private final DataProfileService documentService;
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.DATA_PROFILE + "/{id}")
	public ResponseEntity<DataProfile> findDocumentById(@PathVariable String projectId, @PathVariable String id) {
		return ResponseEntity.ok(documentService.findDocumentById(projectId, id));
	}
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.DATA_PROFILE)
    public ResponseEntity<List<DataProfile>> findDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_id") Optional<String> experimentId,
    														@RequestParam("run_id") Optional<String> runId,
    														@RequestParam("search") Optional<String> search) {
        return ResponseEntity.ok(documentService.findDocumentsByProjectId(projectId, experimentId, runId, search));
    }
	
	@PostMapping("/{projectId}/" + ValidationStorageUtils.DATA_PROFILE)
	public ResponseEntity<DataProfile> createDocument(@PathVariable String projectId, @RequestBody DataProfileDTO request) {
		return ResponseEntity.ok(documentService.createDocument(projectId, request));
	}
	
	@PutMapping("/{projectId}/" + ValidationStorageUtils.DATA_PROFILE + "/{id}")
	public ResponseEntity<DataProfile> updateDocument(@PathVariable String projectId, @PathVariable String id, @RequestBody DataProfileDTO request) {
		return ResponseEntity.ok(documentService.updateDocument(projectId, id, request));
	}
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.DATA_PROFILE + "/{id}")
	public ResponseEntity<Void> deleteDocumentById(@PathVariable String projectId, @PathVariable String id) {
		documentService.deleteDocumentById(projectId, id);
		return ResponseEntity.ok().build();
	}
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.DATA_PROFILE)
    public ResponseEntity<Void> deleteDocuments(@PathVariable String projectId,
    											@RequestParam("experiment_id") Optional<String> experimentId,
    											@RequestParam("run_id") Optional<String> runId) {
		documentService.deleteDocumentsByProjectId(projectId, experimentId, runId);
        return ResponseEntity.ok().build();
    }
}