package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.security.access.prepost.PostFilter;
import org.springframework.stereotype.Service;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
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
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.DataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;
import it.smartcommunitylab.validationstorage.repository.ShortSchemaRepository;
import it.smartcommunitylab.validationstorage.runcomparison.RunSummary;
import lombok.RequiredArgsConstructor;

/**
 * Service for when the UI needs different behavior from the default service for the document.
 */
@Service
@RequiredArgsConstructor
public class UiService {
    private final ProjectRepository projectRepository;
    private final ExperimentRepository experimentRepository;
    private final RunMetadataRepository runMetadataRepository;
    private final ArtifactMetadataRepository artifactMetadataRepository;
    private final DataProfileRepository dataProfileRepository;
    private final DataResourceRepository dataResourceRepository;
    private final RunEnvironmentRepository runEnvironmentRepository;
    private final ShortReportRepository shortReportRepository;
    private final ShortSchemaRepository shortSchemaRepository;
    
    // Project
    @PostFilter(ValidationStorageConstants.POSTFILTER_ID)
    public List<Project> findProjects(Pageable pageable) {
        return projectRepository.findAll(pageable.getSort());
    }

    // Experiment
    public List<Experiment> findExperiments(String projectId, Pageable pageable) {
        return experimentRepository.findByProjectId(projectId, pageable);
    }

    public Experiment findExperimentByExperimentId(String projectId, String experimentId) {
        List<Experiment> documents = experimentRepository.findByProjectIdAndExperimentId(projectId, experimentId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ") was not found.");
    }

    // RunMetadata
    public RunMetadata findRunMetadataByRunId(String projectId, String experimentId, String runId) {
        List<RunMetadata> documents = runMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // ArtifactMetadata
    public List<ArtifactMetadata> findArtifactMetadata(String projectId, String experimentId, String runId, Pageable pageable) {
        return artifactMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId, pageable);
    }

    // DataProfile
    public DataProfile findDataProfileByRunId(String projectId, String experimentId, String runId) {
        List<DataProfile> documents = dataProfileRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // DataResource
    public DataResource findDataResourceByRunId(String projectId, String experimentId, String runId) {
        List<DataResource> documents = dataResourceRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // RunEnvironment
    public RunEnvironment findRunEnvironmentByRunId(String projectId, String experimentId, String runId) {
        List<RunEnvironment> documents = runEnvironmentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // ShortReport
    private ShortReport getShortReport(String projectId, String experimentId, String runId) {
        List<ShortReport> documents = shortReportRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        return null;
    }
    
    public ShortReport findShortReportByRunId(String projectId, String experimentId, String runId) {
        ShortReport document = getShortReport(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
        
        return document;
    }

    // ShortSchema
    public ShortSchema findShortSchemaByRunId(String projectId, String experimentId, String runId) {
        List<ShortSchema> documents = shortSchemaRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }
    
    // RunSummary
    public List<RunSummary> listRunSummaries(String projectId, String experimentId, Pageable pageable) {
        List<RunSummary> runSummaries = new ArrayList<RunSummary>();
        
        List<RunMetadata> runMetadataDocuments = runMetadataRepository.findByProjectIdAndExperimentId(projectId, experimentId, pageable);
        for (RunMetadata runMetadata: runMetadataDocuments)
            runSummaries.add(buildRunSummaryWithShortReport(runMetadata));
        
        return runSummaries;
    }
    
    public RunSummary findRunSummary(String projectId, String experimentId, String runId) {
        RunMetadata runMetadata = findRunMetadataByRunId(projectId, experimentId, runId);
        return buildRunSummaryWithShortReport(runMetadata);
    }
    
    private RunSummary buildRunSummaryWithShortReport(RunMetadata runMetadata) {
        String projectId = runMetadata.getProjectId();
        String experimentId = runMetadata.getExperimentId();
        String runId = runMetadata.getRunId();
        
        ShortReport shortReport = getShortReport(projectId, experimentId, runId);
        
        RunSummary runSummary = new RunSummary(runMetadata.getId(), projectId, experimentId, runId, runMetadata.getCreated());
        runSummary.setRunMetadata(runMetadata);
        runSummary.setShortReport(shortReport);
        
        return runSummary;
    }
}