package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;

public interface ArtifactMetadataRepository extends CrudRepository<ArtifactMetadata, String> {
    List<ArtifactMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
    List<ArtifactMetadata> findByRunId(String runId);
    
    void deleteByProjectId(String projectId);
    
    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
    
    void deleteByRunId(String runId);

//    List<ArtifactMetadata> findByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    List<ArtifactMetadata> findByProjectIdAndRunId(String projectId, String runId);
//
//    List<ArtifactMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
//
//    List<ArtifactMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId, Pageable pageable);
//  
//    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);
//
//    void deleteByProjectIdAndRunId(String projectId, String runId);
//
//    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}