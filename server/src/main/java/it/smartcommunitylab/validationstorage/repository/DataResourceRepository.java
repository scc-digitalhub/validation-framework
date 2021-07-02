package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.DataResource;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface DataResourceRepository extends MongoRepository<DataResource, String> {
    List<DataResource> findByProjectId(String projectId);

    List<DataResource> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<DataResource> findByProjectIdAndRunId(String projectId, String runId);

    List<DataResource> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}