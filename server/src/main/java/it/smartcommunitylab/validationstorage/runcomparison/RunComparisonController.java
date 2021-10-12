package it.smartcommunitylab.validationstorage.runcomparison;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping(value = "/project")
@RequiredArgsConstructor
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class RunComparisonController {
    private final RunComparisonService documentService;
    
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN_COMPARISON + "/{runMetadataIds}")
    public ResponseEntity<RunComparison> compareRuns(
            @PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String[] runMetadataIds) {
        return ResponseEntity.ok(documentService.getComparison(projectId, experimentId, runMetadataIds));
    }
}
