package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.ShortSchema;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface ShortSchemaRepository extends MongoRepository<ShortSchema, String> {
	List<ShortSchema> findByProjectId(String projectId);
	
	List<ShortSchema> findByProjectIdAndExperimentId(String projectId, String experimentId);
	
	List<ShortSchema> findByProjectIdAndRunId(String projectId, String runId);
	
	List<ShortSchema> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}