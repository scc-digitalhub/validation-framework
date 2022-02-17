package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunShortReport;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

public interface RunShortReportRepository extends CrudRepository<RunShortReport, String> {
    
    List<RunShortReport> findByProjectId(String projectId);
    
    List<RunShortReport> findByRunId(String runId);
    
    void deleteByProjectId(String projectId);
    
    void deleteByExperimentId(String experimentId);
    
    void deleteByRunId(String runId);

//    List<RunShortReport> findByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    List<RunShortReport> findByProjectIdAndRunId(String projectId, String runId);
//
//    List<RunShortReport> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
//
//    void deleteByProjectId(String projectId);
//
//    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    void deleteByProjectIdAndRunId(String projectId, String runId);
//
//    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
}