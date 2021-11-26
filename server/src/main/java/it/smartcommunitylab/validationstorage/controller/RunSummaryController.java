package it.smartcommunitylab.validationstorage.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunSummary;
import it.smartcommunitylab.validationstorage.service.RunSummaryService;

/**
 * Controller for end-points related to run summaries.
 */
@RestController
@RequestMapping(value = "/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunSummaryController {
    @Autowired
    private RunSummaryService runSummaryService;
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN)
    public ResponseEntity<List<RunSummary>> listBasicRunSummaries(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            Pageable pageable) {
        return ResponseEntity.ok(runSummaryService.listBasicRunSummaries(projectId, experimentId, pageable));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}")
    public ResponseEntity<RunSummary> getBasicRunSummary(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(runSummaryService.getBasicRunSummary(projectId, experimentId, runId));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_RICH_RECENT)
    public ResponseEntity<List<RunSummary>> listRichRecentRunSummaries(
            @PathVariable String projectId,
            @PathVariable String experimentId) {
        return ResponseEntity.ok(runSummaryService.getRichRecentRunSummaries(projectId, experimentId));
    }
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_RICH + "/{requested}")
    public ResponseEntity<List<RunSummary>> getRichRunSummariesByRunMetadataIds(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable List<String> requested) {
        return ResponseEntity.ok(runSummaryService.getRichRunSummariesByRunMetadataIds(projectId, experimentId, requested));
    }
    
    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN + "/{RunMetadataId}")
    public ResponseEntity<Void> deleteRunByRunMetadataById(@PathVariable String projectId, @PathVariable String RunMetadataId) {
        runSummaryService.deleteRunByRunMetadataId(RunMetadataId);
        return ResponseEntity.ok().build();
    }
}
