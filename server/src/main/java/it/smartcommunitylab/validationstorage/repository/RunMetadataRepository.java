package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

import it.smartcommunitylab.validationstorage.model.RunMetadata;

public interface RunMetadataRepository extends MongoRepository<RunMetadata, String> {
	List<RunMetadata> findByProjectId(String projectId);
	
	List<RunMetadata> findByProjectIdAndExperimentName(String projectId, String experimentName);
	
	List<RunMetadata> findByProjectIdAndRunId(String projectId, String runId);
	
	List<RunMetadata> findByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentName(String projectId, String experimentName);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
}