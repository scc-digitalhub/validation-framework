package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

import it.smartcommunitylab.validationstorage.model.RunMetadata;

public interface RunMetadataRepository extends MongoRepository<RunMetadata, String> {
    List<RunMetadata> findByProjectId(String projectId);

    List<RunMetadata> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<RunMetadata> findByProjectIdAndExperimentId(String projectId, String experimentId, Pageable pageable);

    List<RunMetadata> findByProjectIdAndRunId(String projectId, String runId);

    List<RunMetadata> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}