package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.DataResource;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface DataResourceRepository extends MongoRepository<DataResource, String> {
	List<DataResource> findByProjectId(String projectId);
	
	List<DataResource> findByProjectIdAndExperimentName(String projectId, String experimentName);
	
	List<DataResource> findByProjectIdAndRunId(String projectId, String runId);
	
	List<DataResource> findByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentName(String projectId, String experimentName);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
}