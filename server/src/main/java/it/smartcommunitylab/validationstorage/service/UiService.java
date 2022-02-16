package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
import org.springframework.security.access.prepost.PostFilter;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.RunDataProfile;
import it.smartcommunitylab.validationstorage.model.RunDataResource;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.RunShortReport;
import it.smartcommunitylab.validationstorage.model.RunShortSchema;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunShortReportRepository;
import it.smartcommunitylab.validationstorage.repository.RunShortSchemaRepository;

/**
 * Service for when the UI needs different behavior from the default service for the document.
 */
@Service
public class UiService {
    @Autowired
    private ProjectRepository projectRepository;
    @Autowired
    private ExperimentRepository experimentRepository;
    @Autowired
    private RunMetadataRepository runMetadataRepository;
    @Autowired
    private ArtifactMetadataRepository artifactMetadataRepository;
    @Autowired
    private RunDataProfileRepository dataProfileRepository;
    @Autowired
    private RunDataResourceRepository dataResourceRepository;
    @Autowired
    private RunEnvironmentRepository runEnvironmentRepository;
    @Autowired
    private RunShortReportRepository shortReportRepository;
    @Autowired
    private RunShortSchemaRepository shortSchemaRepository;
    
    // Project
    @PostFilter(ValidationStorageConstants.POSTFILTER_ID)
    public List<Project> findProjects(Pageable pageable) {
        return projectRepository.findAll(pageable.getSort());
    }

    // Experiment
    public List<Experiment> findExperiments(String projectId, Optional<List<String>> tags, Pageable pageable) {
        if (tags.isPresent() && !ObjectUtils.isEmpty(tags.get()))
            return experimentRepository.findByProjectIdAndTagsIn(projectId, tags.get(), pageable);
        return experimentRepository.findByProjectId(projectId, pageable);
    }

    public Experiment findExperimentByExperimentId(String projectId, String experimentId) {
        List<Experiment> documents = experimentRepository.findByProjectIdAndExperimentId(projectId, experimentId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ") was not found.");
    }
    
    // ArtifactMetadata
    public List<ArtifactMetadata> findArtifactMetadata(String projectId, String experimentId, String runId, Pageable pageable) {
        return artifactMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId, pageable);
    }

    // DataProfile
    public RunDataProfile findDataProfileByRunId(String projectId, String experimentId, String runId) {
        List<RunDataProfile> documents = dataProfileRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // DataResource
    public RunDataResource findDataResourceByRunId(String projectId, String experimentId, String runId) {
        List<RunDataResource> documents = dataResourceRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
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
    
    // RunMetadata
    public RunMetadata findRunMetadataByRunId(String projectId, String experimentId, String runId) {
        List<RunMetadata> documents = runMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // ShortReport
    public RunShortReport findShortReportByRunId(String projectId, String experimentId, String runId) {
        List<RunShortReport> documents = shortReportRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }

    // ShortSchema
    public RunShortSchema findShortSchemaByRunId(String projectId, String experimentId, String runId) {
        List<RunShortSchema> documents = shortSchemaRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        throw new DocumentNotFoundException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") was not found.");
    }
}