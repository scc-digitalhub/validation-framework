package it.smartcommunitylab.validationstorage.controller;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.DataProfile;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.ShortReport;
import it.smartcommunitylab.validationstorage.model.ShortSchema;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.service.ArtifactMetadataService;
import it.smartcommunitylab.validationstorage.service.DataProfileService;
import it.smartcommunitylab.validationstorage.service.DataResourceService;
import it.smartcommunitylab.validationstorage.service.ExperimentService;
import it.smartcommunitylab.validationstorage.service.ProjectService;
import it.smartcommunitylab.validationstorage.service.RunEnvironmentService;
import it.smartcommunitylab.validationstorage.service.RunMetadataService;
import it.smartcommunitylab.validationstorage.service.ShortReportService;
import it.smartcommunitylab.validationstorage.service.ShortSchemaService;
import it.smartcommunitylab.validationstorage.service.UiService;

/**
 * Controller for all end-points meant for the UI.
 * Uses UiService for cases that need a specific behavior, otherwise relies on default services for each document.
 */
@RestController
@RequestMapping(value = "/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class UiController {
    @Autowired
    private UiService uiService;

    @Autowired
    private ArtifactMetadataService artifactMetadataService;
    @Autowired
    private ExperimentService experimentService;
    @Autowired
    private DataProfileService dataProfileService;
    @Autowired
    private DataResourceService dataResourceService;
    @Autowired
    private ProjectService projectService;
    @Autowired
    private RunEnvironmentService runEnvironmentService;
    @Autowired
    private RunMetadataService runMetadataService;
    @Autowired
    private ShortReportService shortReportService;
    @Autowired
    private ShortSchemaService shortSchemaService;

    // Project
    @PreAuthorize("permitAll()")
    @GetMapping
    public ResponseEntity<List<Project>> findProjects(Pageable pageable) {
        return ResponseEntity.ok(uiService.findProjects(pageable));
    }

    @PreAuthorize(ValidationStorageConstants.PREAUTH_ID)
    @GetMapping("/{id}")
    public ResponseEntity<Project> findProjectById(@PathVariable String id) {
        return ResponseEntity.ok(projectService.findDocumentById(id));
    }

    @PreAuthorize(ValidationStorageConstants.PREAUTH_REQUEST_ID)
    @PostMapping
    public ResponseEntity<Project> createDocument(@RequestBody @Valid ProjectDTO request, Authentication authentication) {
        return ResponseEntity.ok(projectService.createDocument(request, authentication.getName()));
    }

    @PreAuthorize(ValidationStorageConstants.PREAUTH_ID)
    @PutMapping("/{id}")
    public ResponseEntity<Project> updateDocument(@PathVariable String id, @RequestBody @Valid ProjectDTO request) {
        return ResponseEntity.ok(projectService.updateDocument(id, request));
    }

    @PreAuthorize(ValidationStorageConstants.PREAUTH_ID)
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProjectById(@PathVariable String id) {
        projectService.deleteDocumentById(id);
        return ResponseEntity.ok().build();
    }

    // Experiment
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT)
    public ResponseEntity<List<Experiment>> findExperiments(
            @PathVariable String projectId,
            @RequestParam("tags") Optional<List<String>> tags,
            Pageable pageable) {
        return ResponseEntity.ok(uiService.findExperiments(projectId, tags, pageable));
    }

    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}")
    public ResponseEntity<Experiment> findExperimentByExperimentId(@PathVariable String projectId,
            @PathVariable String experimentId) {
        return ResponseEntity.ok(uiService.findExperimentByExperimentId(projectId, experimentId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{id}")
    public ResponseEntity<Void> deleteExperimentById(@PathVariable String projectId,
            @PathVariable String id) {
        experimentService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    // ArtifactMetadata
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.ARTIFACT_METADATA)
    public ResponseEntity<List<ArtifactMetadata>> findArtifactMetadata(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId,
            Pageable pageable) {
        return ResponseEntity.ok(uiService.findArtifactMetadata(projectId, experimentId, runId, pageable));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.ARTIFACT_METADATA + "/{id}")
    public ResponseEntity<Void> deleteArtifactMetadataById(@PathVariable String projectId, @PathVariable String id) {
        artifactMetadataService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    // DataProfile
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.DATA_PROFILE)
    public ResponseEntity<DataProfile> findDataProfileByRunId(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(uiService.findDataProfileByRunId(projectId, experimentId, runId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.DATA_PROFILE + "/{id}")
    public ResponseEntity<Void> deleteDataProfileById(@PathVariable String projectId, @PathVariable String id) {
        dataProfileService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    // DataResource
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.DATA_RESOURCE)
    public ResponseEntity<DataResource> findDataResourceByRunId(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(uiService.findDataResourceByRunId(projectId, experimentId, runId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.DATA_RESOURCE + "/{id}")
    public ResponseEntity<Void> deleteDataResourceById(@PathVariable String projectId, @PathVariable String id) {
        dataResourceService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    // RunEnvironment
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_ENVIRONMENT)
    public ResponseEntity<RunEnvironment> findRunEnvironmentByRunId(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(uiService.findRunEnvironmentByRunId(projectId, experimentId, runId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN_ENVIRONMENT + "/{id}")
    public ResponseEntity<Void> deleteRunEnvironmentById(@PathVariable String projectId, @PathVariable String id) {
        runEnvironmentService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }
    
    // RunMetadata
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.RUN_METADATA)
    public ResponseEntity<RunMetadata> findRunMetadataByRunId(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(uiService.findRunMetadataByRunId(projectId, experimentId, runId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.RUN_METADATA + "/{id}")
    public ResponseEntity<Void> deleteRunMetadataById(@PathVariable String projectId, @PathVariable String id) {
        runMetadataService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    // ShortReport
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.SHORT_REPORT)
    public ResponseEntity<ShortReport> findShortReportByRunId(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(uiService.findShortReportByRunId(projectId, experimentId, runId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.SHORT_REPORT + "/{id}")
    public ResponseEntity<Void> deleteShortReportById(@PathVariable String projectId, @PathVariable String id) {
        shortReportService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }

    // ShortSchema
    @GetMapping("/{projectId}/" + ValidationStorageConstants.EXPERIMENT + "/{experimentId}/" + ValidationStorageConstants.RUN + "/{runId}/" + ValidationStorageConstants.SHORT_SCHEMA)
    public ResponseEntity<ShortSchema> findShortSchemaByRunId(@PathVariable String projectId,
            @PathVariable String experimentId,
            @PathVariable String runId) {
        return ResponseEntity.ok(uiService.findShortSchemaByRunId(projectId, experimentId, runId));
    }

    @DeleteMapping("/{projectId}/" + ValidationStorageConstants.SHORT_SCHEMA + "/{id}")
    public ResponseEntity<Void> deleteShortSchemaById(@PathVariable String projectId, @PathVariable String id) {
        shortSchemaService.deleteDocumentById(projectId, id);
        return ResponseEntity.ok().build();
    }
}
