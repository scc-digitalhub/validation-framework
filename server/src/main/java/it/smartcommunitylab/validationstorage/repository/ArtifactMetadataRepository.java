package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;

public interface ArtifactMetadataRepository extends MongoRepository<ArtifactMetadata, String> {
    List<ArtifactMetadata> findByProjectId(String projectId);

    List<ArtifactMetadata> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<ArtifactMetadata> findByProjectIdAndRunId(String projectId, String runId);

    List<ArtifactMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    List<ArtifactMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId, Pageable pageable);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}