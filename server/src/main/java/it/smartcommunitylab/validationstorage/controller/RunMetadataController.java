package it.smartcommunitylab.validationstorage.controller;

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
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.service.RunMetadataService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/" + ValidationStorageUtils.RUN_METADATA)
@RequiredArgsConstructor
public class RunMetadataController {
	private final RunMetadataService documentService;
	
	@GetMapping("/{id}")
	public ResponseEntity<RunMetadata> findDocumentById(@PathVariable String id) {
		return ResponseEntity.ok(documentService.findDocumentById(id));
	}
	
	@PostMapping
	public ResponseEntity<RunMetadata> createDocument(@RequestParam String projectId, @RequestBody RunMetadataDTO request) {
		return ResponseEntity.ok(documentService.createDocument(projectId, request));
	}
	
	@PutMapping("/{id}")
	public ResponseEntity<RunMetadata> updateDocument(@PathVariable String id, @RequestBody RunMetadataDTO request) {
		return ResponseEntity.ok(documentService.updateDocument(id, request));
	}
	
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> deleteDocumentById(@PathVariable String id) {
		documentService.deleteDocumentById(id);
		return ResponseEntity.ok().build();
	}
}