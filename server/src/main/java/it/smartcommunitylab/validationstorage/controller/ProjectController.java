package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.ShortReport;
import it.smartcommunitylab.validationstorage.service.ArtifactMetadataService;
import it.smartcommunitylab.validationstorage.service.DataResourceService;
import it.smartcommunitylab.validationstorage.service.RunMetadataService;
import it.smartcommunitylab.validationstorage.service.ShortReportService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/api/project")
@RequiredArgsConstructor
public class ProjectController {
	private final  ArtifactMetadataService artifactMetadataService;
	private final  DataResourceService dataResourceService;
	private final  RunMetadataService runMetadataService;
	private final  ShortReportService shortReportService;
	
	// READ
	@GetMapping("/{projectId}/" + ValidationStorageUtils.ARTIFACT_METADATA)
    public ResponseEntity<List<ArtifactMetadata>> findArtifactMetadataDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
        return ResponseEntity.ok(artifactMetadataService.findDocumentsByProjectId(projectId, experimentName, runId));
    }
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.DATA_RESOURCE)
    public ResponseEntity<List<DataResource>> findDataResourceDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
        return ResponseEntity.ok(dataResourceService.findDocumentsByProjectId(projectId, experimentName, runId));
    }
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.RUN_METADATA)
    public ResponseEntity<List<RunMetadata>> findRunMetadataDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
        return ResponseEntity.ok(runMetadataService.findDocumentsByProjectId(projectId, experimentName, runId));
    }
	
	@GetMapping("/{projectId}/" + ValidationStorageUtils.SHORT_REPORT)
    public ResponseEntity<List<ShortReport>> findShortReportDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
        return ResponseEntity.ok(shortReportService.findDocumentsByProjectId(projectId, experimentName, runId));
    }
	
	// DELETE
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.ARTIFACT_METADATA)
    public ResponseEntity<Void> deleteArtifactMetadataDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
        artifactMetadataService.deleteDocumentsByProjectId(projectId, experimentName, runId);
        return ResponseEntity.ok().build();
    }
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.DATA_RESOURCE)
    public ResponseEntity<Void> deleteDataResourceDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
        dataResourceService.deleteDocumentsByProjectId(projectId, experimentName, runId);
        return ResponseEntity.ok().build();
    }
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.RUN_METADATA)
    public ResponseEntity<Void> deleteRunMetadataDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
		runMetadataService.deleteDocumentsByProjectId(projectId, experimentName, runId);
        return ResponseEntity.ok().build();
    }
	
	@DeleteMapping("/{projectId}/" + ValidationStorageUtils.SHORT_REPORT)
    public ResponseEntity<Void> deleteShortReportDocuments(@PathVariable String projectId,
    														@RequestParam("experiment_name") Optional<String> experimentName,
    														@RequestParam("run_id") Optional<String> runId) {
		shortReportService.deleteDocumentsByProjectId(projectId, experimentName, runId);
        return ResponseEntity.ok().build();
    }
}
