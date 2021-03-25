package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.ShortReport;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface ShortReportRepository extends MongoRepository<ShortReport, String> {
	List<ShortReport> findByProjectId(String projectId);
	
	List<ShortReport> findByProjectIdAndExperimentId(String projectId, String experimentId);
	
	List<ShortReport> findByProjectIdAndRunId(String projectId, String runId);
	
	List<ShortReport> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}