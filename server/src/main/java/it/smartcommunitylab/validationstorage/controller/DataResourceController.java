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
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.service.DataResourceService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/" + ValidationStorageUtils.DATA_RESOURCE)
@RequiredArgsConstructor
public class DataResourceController {
	private final DataResourceService documentService;
	
	@GetMapping("/{id}")
	public ResponseEntity<DataResource> findDocumentById(@PathVariable String id) {
		return ResponseEntity.ok(documentService.findDocumentById(id));
	}
	
	@PostMapping
	public ResponseEntity<DataResource> createDocument(@RequestParam String projectId, @RequestBody DataResourceDTO request) {
		return ResponseEntity.ok(documentService.createDocument(projectId, request));
	}
	
	@PutMapping("/{id}")
	public ResponseEntity<DataResource> updateDocument(@PathVariable String id, @RequestBody DataResourceDTO request) {
		return ResponseEntity.ok(documentService.updateDocument(id, request));
	}
	
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> deleteDocumentById(@PathVariable String id) {
		documentService.deleteDocumentById(id);
		return ResponseEntity.ok().build();
	}
}