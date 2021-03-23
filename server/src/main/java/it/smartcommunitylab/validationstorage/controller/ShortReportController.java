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
import it.smartcommunitylab.validationstorage.model.ShortReport;
import it.smartcommunitylab.validationstorage.model.dto.ShortReportDTO;
import it.smartcommunitylab.validationstorage.service.ShortReportService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/" + ValidationStorageUtils.SHORT_REPORT)
@RequiredArgsConstructor
public class ShortReportController {
	private final ShortReportService documentService;
	
	@GetMapping("/{id}")
	public ResponseEntity<ShortReport> findDocumentById(@PathVariable String id) {
		return ResponseEntity.ok(documentService.findDocumentById(id));
	}
	
	@PostMapping
	public ResponseEntity<ShortReport> createDocument(@RequestParam String projectId, @RequestBody ShortReportDTO request) {
		return ResponseEntity.ok(documentService.createDocument(projectId, request));
	}
	
	@PutMapping("/{id}")
	public ResponseEntity<ShortReport> updateDocument(@PathVariable String id, @RequestBody ShortReportDTO request) {
		return ResponseEntity.ok(documentService.updateDocument(id, request));
	}
	
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> deleteDocumentById(@PathVariable String id) {
		documentService.deleteDocumentById(id);
		return ResponseEntity.ok().build();
	}
}