package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Pageable;
import org.springframework.security.access.prepost.PostFilter;
import org.springframework.stereotype.Service;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
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
	
	// Project
	@PostFilter(ValidationStorageUtils.POSTFILTER_ID)
	public List<Project> findProjects(Pageable pageable) {
		return projectRepository.findAll(pageable.getSort());
	}
	
	// Experiment
	public List<Experiment> findExperiments(String projectId, Optional<String> experimentId, Pageable pageable) {
		if (experimentId.isPresent())
			return experimentRepository.findByProjectIdAndExperimentId(projectId, experimentId.get());
		else
			return experimentRepository.findByProjectId(projectId, pageable);
	}
	
	// RunMetadata
	public List<RunMetadata> findRunMetadata(String projectId, String experimentId, Optional<String> runId, Pageable pageable) {
		if (runId.isPresent())
			return runMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId.get());
		else
			return runMetadataRepository.findByProjectIdAndExperimentId(projectId, experimentId, pageable);
	}
	
	// ArtifactMetadata
	public List<ArtifactMetadata> findArtifactMetadata(String projectId, String experimentId, String runId, Pageable pageable) {
		return artifactMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId, pageable);
	}
}
