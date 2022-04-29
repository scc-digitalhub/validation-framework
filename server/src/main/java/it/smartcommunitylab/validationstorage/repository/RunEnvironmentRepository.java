package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunEnvironment;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface RunEnvironmentRepository extends JpaRepository<RunEnvironment, String> {
    
    List<RunEnvironment> findByProjectId(String projectId);
    
    Optional<RunEnvironment> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
    void deleteByProjectId(String projectId);
    
    void deleteByExperimentId(String experimentId);
    
    void deleteByRunId(String runId);
    
    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

//    List<RunEnvironment> findByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    List<RunEnvironment> findByProjectIdAndRunId(String projectId, String runId);
//
//    List<RunEnvironment> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
//
//    void deleteByProjectId(String projectId);
//
//    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    void deleteByProjectIdAndRunId(String projectId, String runId);
//
//    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
}