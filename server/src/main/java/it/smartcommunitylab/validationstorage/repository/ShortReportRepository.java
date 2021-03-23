package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.ShortReport;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface ShortReportRepository extends MongoRepository<ShortReport, String> {
	List<ShortReport> findByProjectId(String projectId);
	
	List<ShortReport> findByProjectIdAndExperimentName(String projectId, String experimentName);
	
	List<ShortReport> findByProjectIdAndRunId(String projectId, String runId);
	
	List<ShortReport> findByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
	
	void deleteByProjectId(String projectId);
	
	void deleteByProjectIdAndExperimentName(String projectId, String experimentName);
	
	void deleteByProjectIdAndRunId(String projectId, String runId);
	
	void deleteByProjectIdAndExperimentNameAndRunId(String projectId, String experimentName, String runId);
}