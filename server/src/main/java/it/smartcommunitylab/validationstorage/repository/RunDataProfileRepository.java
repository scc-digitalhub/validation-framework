package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunDataProfile;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface RunDataProfileRepository extends JpaRepository<RunDataProfile, String> {
    
    List<RunDataProfile> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
    List<RunDataProfile> findByRunId(String runId);
    
    void deleteByProjectId(String projectId);
    
    void deleteByExperimentId(String experimentId);
    
    void deleteByRunId(String runId);
    
    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

//    List<RunDataProfile> findByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    List<RunDataProfile> findByProjectIdAndRunId(String projectId, String runId);
//
//    List<RunDataProfile> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
//
//    void deleteByProjectId(String projectId);
//
//    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    void deleteByProjectIdAndRunId(String projectId, String runId);
//
//    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
}