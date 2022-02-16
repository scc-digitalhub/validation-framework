package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunDataResource;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.CrudRepository;

public interface RunDataResourceRepository extends CrudRepository<RunDataResource, String> {
    List<RunDataResource> findByProjectId(String projectId);

    List<RunDataResource> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<RunDataResource> findByProjectIdAndRunId(String projectId, String runId);

    List<RunDataResource> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}