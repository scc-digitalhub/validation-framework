package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunShortSchema;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.CrudRepository;

public interface RunShortSchemaRepository extends CrudRepository<RunShortSchema, String> {
    List<RunShortSchema> findByProjectId(String projectId);

    List<RunShortSchema> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<RunShortSchema> findByProjectIdAndRunId(String projectId, String runId);

    List<RunShortSchema> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}