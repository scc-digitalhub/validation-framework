package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunDataSchema;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

public interface RunDataSchemaRepository extends CrudRepository<RunDataSchema, String> {
    
    List<RunDataSchema> findByProjectId(String projectId);
    
    List<RunDataSchema> findByRunId(String runId);
    
    void deleteByProjectId(String projectId);
    
    void deleteByExperimentId(String experimentId);
    
    void deleteByRunId(String runId);

//    List<RunShortSchema> findByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    List<RunShortSchema> findByProjectIdAndRunId(String projectId, String runId);
//
//    List<RunShortSchema> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
//
//    void deleteByProjectId(String projectId);
//
//    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    void deleteByProjectIdAndRunId(String projectId, String runId);
//
//    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
}