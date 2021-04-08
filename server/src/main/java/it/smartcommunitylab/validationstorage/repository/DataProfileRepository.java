package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.DataProfile;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface DataProfileRepository extends MongoRepository<DataProfile, String> {
	List<DataProfile> findByProjectId(String projectId);
	
	List<DataProfile> findByProjectIdAndExperimentId(String projectId, String experimentId);
	
	List<DataProfile> findByProjectIdAndRunId(String projectId, String runId);
	
	List<DataProfile> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}