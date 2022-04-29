package it.smartcommunitylab.validationstorage.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylab.validationstorage.model.RunMetadata;

public interface RunMetadataRepository extends JpaRepository<RunMetadata, String> {
    
    List<RunMetadata> findByProjectId(String projectId);
    
    Optional<RunMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
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