package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunEnvironment;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface RunEnvironmentRepository extends MongoRepository<RunEnvironment, String> {
    List<RunEnvironment> findByProjectId(String projectId);

    List<RunEnvironment> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<RunEnvironment> findByProjectIdAndRunId(String projectId, String runId);

    List<RunEnvironment> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}