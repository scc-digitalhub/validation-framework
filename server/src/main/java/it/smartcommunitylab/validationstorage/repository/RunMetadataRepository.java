package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.RunMetadata;

public interface RunMetadataRepository extends CrudRepository<RunMetadata, String> {
    
    List<RunMetadata> findByProjectId(String projectId);
    
    List<RunMetadata> findByProjectIdAndRunId(String projectId, String runId);
    
    void deleteByProjectId(String projectId);
    
    void deleteByExperimentId(String experimentId);
    
    void deleteByRunId(String runId);
    
    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

//    List<RunMetadata> findByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    List<RunMetadata> findByProjectIdAndExperimentId(String projectId, String experimentId, Pageable pageable);
//
//    List<RunMetadata> findByProjectIdAndRunId(String projectId, String runId);
//
//    List<RunMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
//
//    void deleteByProjectId(String projectId);
//
//    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    void deleteByProjectIdAndRunId(String projectId, String runId);
//
//    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
}