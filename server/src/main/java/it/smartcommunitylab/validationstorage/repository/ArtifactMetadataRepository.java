package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;

public interface ArtifactMetadataRepository extends MongoRepository<ArtifactMetadata, String> {
	List<ArtifactMetadata> findByProjectId(String projectId);
	
	List<ArtifactMetadata> findByProjectIdAndExperimentName(String projectId, String experimentName);
	
	List<ArtifactMetadata> findByProjectIdAndRunId(String projectId, String runId);
	
	List<ArtifactMetadata> findByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentName(String projectId, String experimentName);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
}